# Model Training Pipeline

## Dataset
StateFarm Distracted Driver Dataset (public, kaggle). Contains labeled images of drivers performing actions in the 10 classes:
- c0: safe driving
- c1: texting - right
- c2: talking on the phone - right
- c3: texting - left
- c4: talking on the phone - left
- c5: operating the radio
- c6: drinking
- c7: reaching behind
- c8: hair and makeup
- c9: talking to passenger

Data has been pre-separated into test and train

## Notebooks
data_exploration
model_comparison
onnx_export_and_quant.ipynb

## Model Comparison details
Models were trained for up to 20 epochs, with checkpoints and early stop if validation accuracy failed to improve for 5 epochs in a row.  
Model selection compared not just accuracy, but size and latency, to allow consideration for edge deployment.