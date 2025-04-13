import os
import nibabel as nib
import numpy as np
from pathlib import Path
from scipy.ndimage import zoom
from nipype.interfaces.fsl import BET
from nipype.interfaces.ants import N4BiasFieldCorrection
from monai.transforms import (
    Spacing,
    Resize,
    NormalizeIntensity,
    SpatialResample,
)
from tqdm import tqdm

class WMHPreprocessor:
    def __init__(self, data_root):
        self.data_root = Path(data_root)
        self.target_spacing = (0.95833331, 0.95833334, 2.99999717)  # mm
        self.target_size = (240, 240, 48)

    def skull_strip(self, image_path):
        """Apply FSL BET for skull stripping"""
        try:
            bet = BET()
            bet.inputs.in_file = str(image_path)
            bet.inputs.frac = 0.5
            bet.inputs.robust = True
            bet.inputs.mask = True
            result = bet.run()
            return nib.load(result.outputs.out_file).get_fdata()
        except Exception as e:
            print(f"Warning: FSL BET not available. Using simple intensity-based brain extraction instead. Error: {str(e)}")
            # Fallback to simple intensity-based brain extraction
            img = nib.load(str(image_path))
            data = img.get_fdata()
            # Simple thresholding-based brain extraction
            brain_mask = data > np.percentile(data[data > 0], 10)
            return data * brain_mask

    def normalize_intensity(self, image):
        """Z-score normalization within brain mask"""
        brain_mask = image > 0
        mean = np.mean(image[brain_mask])
        std = np.std(image[brain_mask])
        normalized = (image - mean) / (std + 1e-8)
        return normalized * brain_mask

    def resample_to_spacing(self, data, original_spacing, target_spacing, tolerance=0.05):
        """
        Resample image to target spacing if different enough
        tolerance: fractional difference allowed (5% by default)
        """
        # Check if spacing is already close enough
        spacing_diff = np.abs(np.array(original_spacing) - np.array(target_spacing)) / np.array(target_spacing)
        if np.all(spacing_diff < tolerance):
            print(f"Skipping resampling: current spacing {original_spacing} close to target {target_spacing}")
            return data
        
        # Calculate scale factors
        scale_factors = [o/t for o, t in zip(original_spacing, target_spacing)]
        return zoom(data, scale_factors, order=3)

    def process_single_file(self, input_path: Path, output_path: Path, overwrite: bool = False):
        """Process a single .nii.gz file"""
        if input_path == output_path:
            raise ValueError("Input and output paths cannot be identical")
        if not input_path.exists() or not str(input_path).endswith('.nii.gz'):
            return None
        if not overwrite and output_path.exists():
            return output_path
        
        try:
            # Load image
            img = nib.load(str(input_path))
            original_spacing = img.header.get_zooms()
            print(f"Original spacing: {original_spacing}")
            
            # Determine modality from filename
            filename = input_path.name.lower()
            is_mask = 'mask' in filename or 'wmh' in filename
            
            # Process based on whether it's a mask or not
            if is_mask:
                # Masks don't need skull stripping or intensity normalization
                data = img.get_fdata()
            else:
                # Regular images need full processing
                data = self.skull_strip(input_path)
                data = self.normalize_intensity(data)
            
            # Resample only if spacing is significantly different
            data_resampled = self.resample_to_spacing(
                data, original_spacing, self.target_spacing
            )
            # Resize to target size
            # data_resampled = self.resize_to_size(data_resampled, self.target_size)
            
            # Save with appropriate processing for masks
            if is_mask:
                # Convert boolean to uint8 (0 and 1)
                mask_data = (data_resampled > 0.5).astype(np.uint8)
                nib.save(
                    nib.Nifti1Image(mask_data, np.eye(4)),
                    str(output_path)
                )
            else:
                nib.save(
                    nib.Nifti1Image(data_resampled, np.eye(4)),
                    str(output_path)
                )
            
            return output_path
        
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")
            return None

    def process_dataset(self):
        """Process all .nii.gz files in the dataset"""
        # Find all .nii.gz files recursively
        all_t1_files = list(self.data_root.rglob("*/pre/T1.nii.gz"))
        all_flair_files = list(self.data_root.rglob("*/pre/FLAIR.nii.gz"))
        all_files = all_t1_files + all_flair_files
        all_files.sort(key=lambda x: str(x))
        
        def get_output_path(file_path):
            # /pre/T1.nii.gz -> /pre2/T1.nii.gz
            return file_path.parent.parent / "pre2" / file_path.name
        
        # Process files with progress tracking
        for file_path in tqdm(all_files, desc="Processing files"):

            # Skip files that are already in a 'preprocessed' directory
            output_path = get_output_path(file_path)
            if output_path.exists() or output_path == file_path:
                print(f"Skipping: {file_path.relative_to(self.data_root)}")
                continue
            output_path.parent.mkdir(exist_ok=True, parents=True)
            
            print(f"\nProcessing: {file_path.relative_to(self.data_root)}")
            output_path = self.process_single_file(file_path, output_path)
            
            if output_path:
                print(f"Saved to: {output_path.relative_to(self.data_root)}")
            else:
                print(f"Failed to process: {file_path.relative_to(self.data_root)}")
            

if __name__ == "__main__":

    preprocessor = WMHPreprocessor(data_root="/Users/hsuh/Gitrepo/SwitchSite/1.data/MICCAI-2017")
    
    preprocessor.process_dataset()
