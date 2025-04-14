# Product Development

## Competitor Service Review  

In the clinical market, several FDA-cleared software solutions offer automated WMH (lesion) segmentation as part of comprehensive neuroimaging analysis. Below we review two prominent services and their features:

### NeuroQuant MS (by Cortechs.ai)  
NeuroQuant® MS is an extension of the NeuroQuant platform focused on multiple sclerosis lesion analysis. It was formerly known as **LesionQuant** and has been in clinical use for over a decade. NeuroQuant MS combines a patient’s 3D T1-weighted MRI and T2-FLAIR MRI to automatically identify and quantify white matter lesions, integrating these results with brain volumetry. Key aspects of this service include: 

- **Automated Lesion Segmentation:** Detects and segments FLAIR hyperintense lesions throughout the brain white matter. The software produces a lesion mask overlay on the MRI, distinguishing regions like periventricular, juxtacortical, infratentorial, and deep white matter lesions [1]. It leverages a hybrid algorithm (machine learning combined with a deep learning CNN in the latest version) to improve accuracy of lesion detection [2].  

- **Quantitative Reports:** Provides volumetric measurements of total lesion load (in cubic centimeters) and lesion count, plus regional lesion volumes. It also tracks longitudinal changes – for example, reporting new or enlarging lesions and percent change in lesion volume between scans [5]. Results are presented in a clear report with tables and color-coded brain images, and can be sent directly to PACS as DICOM series for radiologist review.  

- **Brain Structure Volumetry:** In addition to WMH, NeuroQuant MS outputs brain structure volumes (e.g. hippocampus, ventricles, cortical gray/white matter) and an **atrophy assessment**. It compares the patient’s brain volumes and lesion load against a normative database of healthy individuals matched for age, sex, and intracranial volume [1,3]. This context helps clinicians interpret whether brain volume loss or lesion burden is excessive for the patient’s demographic.

- **Clinical Integration:** The software is installed on-site or accessed via a secure cloud; it can process a brain MRI study in about 5–7 minutes and automatically return results to the radiologist’s workstation [3]. NeuroQuant was the first FDA-cleared tool for brain MRI quantification [3], and NeuroQuant MS (LesionQuant) is FDA 510(k) cleared (Class II) and CE-marked (Class IIa) for clinical use [4]. It has been used in routine practice since around 2006 [1,3]. This product is part of the “icobrain” suite which has modules for other conditions (e.g. dementia, traumatic brain injury), but icobrain MS is specifically tailored to MS lesions.

Overall, NeuroQuant MS provides an end-to-end solution for MS lesion segmentation and brain volumetric analysis. Its strength lies in fast, reproducible results and integration with PACS workflow. The hybrid algorithm update in recent versions aims to ensure high sensitivity to lesions while minimizing false positives, even in difficult areas near the cortex or ventricles.

### icobrain MS (by Icometrix)  
icobrain MS is a cloud-based AI service for quantitative brain MRI analysis in multiple sclerosis. Developed by Icometrix, it has gained wide adoption in hospitals as a tool to objectively measure both brain atrophy and lesion burden from standard MRI scans. Key features of icobrain MS include:

- **Lesion and Atrophy Analysis:** Automatically segments MS white matter lesions on FLAIR MRI and calculates brain tissue volumes. The input to icobrain MS is a 3D FLAIR and 3D T1 scan for each patient [5]. The output includes a segmentation mask for lesions and numerical values for total lesion volume and count. Additionally, it computes annualized percentage brain volume change (PBVC) for whole brain and gray matter, which is crucial for monitoring neurodegeneration in MS [5].  
- **Cloud-Based Pipeline:** The analysis is performed on Icometrix’s secure cloud platform (compliant with medical data security standards). After an MRI is acquired, images are uploaded (automatically or on-demand) to the cloud where icobrain MS processes them, typically in >10 minutes per case [5]. Results are then delivered back to the user. This cloud deployment means updates to the AI models can be rolled out centrally, and heavy computations don’t burden local infrastructure.  
- **Reporting and Integration:** icobrain MS returns DICOM segmentation overlays (for radiologists to visualize lesions in the MRI slices) and a concise report. The report summarizes brain volumes, lesion volumes, and highlights any changes since the prior scan, alongside reference percentiles from an age- and sex-matched healthy population [5]. The service integrates with radiology workflows via PACS or hospital AI marketplaces (e.g. GE Healthcare Edison, Philips Intellispace) for seamless case submission and result retrieval [5].  

- **Regulatory Approval and Usage:** The icobrain MS software is FDA 510(k) cleared and CE-marked (Class II medical device) for clinical use [5]. It has been on the market since 2016 and, as of 2024, is used in over 100 clinics worldwide and hundreds of research centers [5]. This product is part of the “icobrain” suite which has modules for other conditions (e.g. dementia, traumatic brain injury), but icobrain MS is specifically tailored to MS lesions.

- **Technical Approach:** Icometrix continually improves the algorithm powering icobrain MS. Version 5.1 of the product introduced a novel combined segmentation approach: an unsupervised intensity-based method is run in parallel with a supervised deep learning model (a 3D U-Net with attention gates), and their outputs are fused [6]. This hybrid technique capitalizes on the strengths of both methods – the traditional model provides consistency and low false-positives in typical lesion areas, while the CNN specializes in catching lesions in atypical locations like the brainstem or cortex [6]. The result was a reported improvement in detecting infratentorial lesions by 14% and juxtacortical lesions by 31%, compared to the older method alone [6]. Such enhancements underscore the company’s focus on validation: multiple studies have been published verifying icobrain’s lesion segmentation accuracy and consistency over time against expert manual segmentations [5].

In summary, icobrain MS offers an advanced, cloud-based solution for WMH/MS lesion segmentation with strong regulatory credentials. Its ability to track brain atrophy in tandem with lesions, and its integration into clinical systems, make it a powerful tool for neurologists and radiologists managing MS patients. The ongoing algorithm improvements (combining AI methods) suggest that its performance in identifying subtle lesions will continue to improve, further aligning the software’s output with radiological ground truth.

## Proposal

`Our goal is to create a clinical decision support system that enhances, rather than replaces, the diagnostic process carried out by medical professionals.` The emphasis is on improving efficiency and supporting doctors in cases where they most need it.

### Product Vision
This system will deliver automated WMH lesion segmentation and brain volumetric analysis, integrated directly into clinical workflows. The primary utility is in triaging and prioritizing scans that require deeper human review, particularly those involving ambiguous or borderline findings.

### Core Features & Roadmap
- **Strengthen Edge Cases**: Most expert discussions center around uncertain or `borderline findings`. Our pipeline will include a mechanism to flag such edge cases through `anomaly detection` or uncertainty estimation. Also focus on the `fine-tuning model` that works better on edge cases but not necessarily on the overall accuracy.

- **Bootstrapping Indicators**: Introduce new <u>indicators</u> driven from the model's internal layers to assist the radiologist in reviewing the results faster and intuitively.

- **Multimodal Chatbot**: Leverage vision-large language models (`vLLMs`) to generate natural-language descriptions of segmentation results. It will write a report based on the segmentation results in the initial version, and later it will be able to `discuss the reasoning` behind the segmentation with the radiologist. It does not need to be in house foundation model, but can be leverage on third party models or APIs.

- **Clinical Integration**: Export results as `DICOM` overlays and generate structured reports compatible with `PACS` systems.

### Summary
Rather than only chanllenging for clinical judgment accuracy scores, the proposed solution aims to assist radiologists and neurologists by highlighting edge cases, improving interpretability, and saving time. This strategic enhancement in workflow efficiency and confidence will serve as a strong differentiator in product adoption.


### References

[1] [Commercial volumetric MRI reporting tools in multiple sclerosis: a systematic review of the evidence](https://discovery.ucl.ac.uk/id/eprint/10158877/1/s00234-022-03074-w.pdf#:~:text=3D%20T1%20and%202D%20or,range%203%E2%80%93100%20y%2C%20equal%20male%2Ffemale)

[2] [NeuroQuant 4.0: Improved segmentation - Cortechs.ai](https://www.cortechs.ai/neuroquant-4-0-improved-segmentation-with-new-hybrid-ml-dl-model/#:~:text=Similar%20to%20the%20improvements%20outlined,learning%20and%20deep%20learning%20techniques)

[3] [Cortechs.ai NeuroQuant & LesionQuant](https://au.getzhealthcare.com/products/neuro/neuro-surgery/ai-software/cortechs.ai-neuroquant-lesionquant#:~:text=NeuroQuant%20MS%2C%20the%20automated%20lesion,Sclerosis%20and%20other%20neurodegenerative%20diseases)

[4] [NeuroQuant MS - Cortechs.ai](https://healthairegister.com/products/cortechs-ai-neuroquant-ms/#:~:text=Certification%20CE)

[5] [icobrain ms - icometrix](https://healthairegister.com/products/icometrix-icobrain-ms/#:~:text=Data%20characteristics%20Population%20multiple%20sclerosis,PACS%29%2C%20Integration%20RIS)

[6] [icobrain ms 5.1: Combining unsupervised and supervised approaches for improving the detection of multiple sclerosis lesions - PubMed](https://pubmed.ncbi.nlm.nih.gov/34111718/#:~:text=automatic%20combined%20method%2C%20based%20on,namely%20difficulties%20in%20segmenting%20infratentorial)
