import numpy as np
from scipy.spatial.distance import directed_hausdorff
from typing import Tuple, Dict, Union, List
import numpy.typing as npt

def dice_coefficient(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Dice Similarity Coefficient (DSC)
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Dice coefficient between 0 and 1
    """
    intersection = np.sum(y_true * y_pred)
    return (2. * intersection) / (np.sum(y_true) + np.sum(y_pred))

def sensitivity(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Sensitivity (True Positive Rate)
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Sensitivity between 0 and 1
    """
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    actual_positives = np.sum(y_true == 1)
    return true_positives / actual_positives if actual_positives > 0 else 0.0

def specificity(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Specificity (True Negative Rate)
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Specificity between 0 and 1
    """
    true_negatives = np.sum((y_true == 0) & (y_pred == 0))
    actual_negatives = np.sum(y_true == 0)
    return true_negatives / actual_negatives if actual_negatives > 0 else 0.0

def precision(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Precision (Positive Predictive Value)
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Precision between 0 and 1
    """
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    predicted_positives = np.sum(y_pred == 1)
    return true_positives / predicted_positives if predicted_positives > 0 else 0.0

def f1_score(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate F1 Score (harmonic mean of precision and recall)
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: F1 score between 0 and 1
    """
    prec = precision(y_true, y_pred)
    rec = sensitivity(y_true, y_pred)
    return 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

def average_volume_difference(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Average Volume Difference
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Average volume difference
    """
    true_volume = np.sum(y_true)
    pred_volume = np.sum(y_pred)
    return abs(true_volume - pred_volume) / true_volume if true_volume > 0 else 0.0

def hausdorff_distance(y_true: npt.NDArray, y_pred: npt.NDArray) -> float:
    """
    Calculate Hausdorff Distance
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        float: Hausdorff distance
    """
    # Get coordinates of non-zero elements
    true_coords = np.argwhere(y_true)
    pred_coords = np.argwhere(y_pred)
    
    if len(true_coords) == 0 or len(pred_coords) == 0:
        return 0.0
    
    # Calculate directed Hausdorff distances
    h1 = directed_hausdorff(true_coords, pred_coords)[0]
    h2 = directed_hausdorff(pred_coords, true_coords)[0]
    
    return max(h1, h2)

def lesion_wise_false_positives(y_true: npt.NDArray, y_pred: npt.NDArray) -> int:
    """
    Count lesion-wise false positives
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        int: Number of false positive lesions
    """
    from scipy.ndimage import label
    
    # Label connected components in prediction
    labeled_pred, num_pred = label(y_pred)
    
    # Count false positives (predicted lesions with no overlap with true lesions)
    false_positives = 0
    for i in range(1, num_pred + 1):
        pred_lesion = (labeled_pred == i)
        if np.sum(y_true[pred_lesion]) == 0:
            false_positives += 1
            
    return false_positives

def evaluate_segmentation(y_true: npt.NDArray, y_pred: npt.NDArray) -> Dict[str, float]:
    """
    Evaluate segmentation performance using multiple metrics
    
    Args:
        y_true: Ground truth binary mask
        y_pred: Predicted binary mask
        
    Returns:
        Dict containing all evaluation metrics
    """
    metrics = {
        'dice': dice_coefficient(y_true, y_pred),
        'sensitivity': sensitivity(y_true, y_pred),
        'specificity': specificity(y_true, y_pred),
        'precision': precision(y_true, y_pred),
        'f1_score': f1_score(y_true, y_pred),
        'volume_difference': average_volume_difference(y_true, y_pred),
        'hausdorff_distance': hausdorff_distance(y_true, y_pred),
        'false_positives': lesion_wise_false_positives(y_true, y_pred)
    }
    
    return metrics

def evaluate_batch(y_true_batch: npt.NDArray, y_pred_batch: npt.NDArray) -> Dict[str, float]:
    """
    Evaluate a batch of segmentations
    
    Args:
        y_true_batch: Batch of ground truth binary masks
        y_pred_batch: Batch of predicted binary masks
        
    Returns:
        Dict containing average metrics across the batch
    """
    batch_metrics = []
    
    for y_true, y_pred in zip(y_true_batch, y_pred_batch):
        metrics = evaluate_segmentation(y_true, y_pred)
        batch_metrics.append(metrics)
    
    # Calculate mean metrics across the batch
    mean_metrics = {}
    for metric_name in batch_metrics[0].keys():
        mean_metrics[metric_name] = np.mean([m[metric_name] for m in batch_metrics])
    
    return mean_metrics 