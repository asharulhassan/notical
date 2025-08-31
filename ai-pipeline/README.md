# NOTICAL AI Pipeline - Clean Start

A simple, clean AI pipeline for flashcard generation built from scratch.

## Structure

```
ai-pipeline/
├── data/           # Training/testing data
├── models/         # Trained models
├── src/            # Source code
└── requirements.txt
```

## The 3 Steps

1. **Data Preprocessing** ✅ - Load, clean, and split data (80% train, 20% test)
2. **Model Creation** 🔄 - Build and train the AI model
3. **Evaluation** 🔄 - Test and evaluate the model

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run data preprocessing:
```bash
python src/data_preprocessing.py
```

This will:
- Load sample data (replace with your actual data)
- Clean the data
- Split 80% training, 20% testing
- Save the split data to `data/` folder

## Current Status

- ✅ **Step 1 Complete**: Data preprocessing with 80/20 split
- 🔄 **Step 2**: Model creation (next)
- 🔄 **Step 3**: Model evaluation (after step 2)

## Next Steps

1. Test the data preprocessing
2. Build the model architecture
3. Train the model
4. Evaluate performance
