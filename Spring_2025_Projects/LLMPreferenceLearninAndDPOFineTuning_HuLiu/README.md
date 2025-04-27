# LLM Preference Learning and DPO Fine-tuning

## 🌟 Overview

This project demonstrates a comprehensive approach to improving Large Language Model (LLM) performance through preference learning and Direct Preference Optimization (DPO). We use two distinct methods to create preference datasets:

1. **LLM Judge-Based Collection**: Implementing a sophisticated judging system to evaluate response quality
2. **PairRM-Based Collection**: Utilizing the PairRM algorithm to create preference pairs

The collected preference data is then used to fine-tune Llama-3.2 models using the DPO technique, significantly improving response quality across various metrics.

## 🚀 Key Features

- Data generation and preference collection from Lima dataset
- Implementation of an LLM-based judging system
- Application of PairRM for preference pair creation
- DPO fine-tuning of Llama-3.2-1B
- Iterative training approach for model improvement
- Comprehensive evaluation and comparative analysis
- HuggingFace dataset and model integration

## 📋 Requirements

- Python 3.8+
- PyTorch 2.0+
- Transformers 4.30+
- PEFT
- Accelerate
- llm-blender
- Datasets
- tqdm
- numpy
- pandas
- matplotlib

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/llm-preference-learning.git
cd llm-preference-learning

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🏗️ Project Structure

```
llm-preference-learning/
├── data/
│   ├── raw/                  # Original Lima dataset
│   ├── processed/            # Processed instructions and responses
│   ├── judge_dataset/        # LLM judge-based preference pairs
│   └── pairm_dataset/        # PairRM-based preference pairs
├── models/
│   ├── base/                 # Base Llama-3.2 model
│   ├── lora_adapter_judge/   # LoRA adapter for judge-based DPO
│   └── lora_adapter_pair/    # LoRA adapter for PairRM-based DPO
├── notebooks/
│   ├── data_generation.ipynb      # Dataset generation process
│   ├── model_training.ipynb       # DPO training process
│   └── evaluation.ipynb           # Model evaluation
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_loader.py        # Functions for loading datasets
│   │   └── data_processor.py     # Functions for data cleaning and processing
│   ├── judge/
│   │   ├── __init__.py
│   │   ├── judge_prompt.py       # LLM judge prompt templates
│   │   └── judge_system.py       # Implementation of judging system
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_loader.py       # Functions for loading models
│   │   └── training.py           # Training utilities
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py            # Helper functions
│   └── main.py                   # Main execution script
├── scripts/
│   ├── generate_responses.py     # Script to generate model responses
│   ├── create_judge_dataset.py   # Script to create judge-based dataset
│   ├── create_pairm_dataset.py   # Script to create PairRM dataset
│   ├── train_dpo_judge.py        # Script to train judge-based DPO model
│   └── train_dpo_pairm.py        # Script to train PairRM-based DPO model
├── requirements.txt              # Project dependencies
├── setup.py                      # Package setup file
├── LICENSE                       # Project license
└── README.md                     # Project overview (this file)
```

## 📊 Usage

### 1. Dataset Generation

#### a) Generate Base Responses

```bash
python scripts/generate_responses.py \
    --model "meta-llama/Llama-3.2-1B-chat" \
    --dataset "GAIR/lima" \
    --num_instructions 50 \
    --responses_per_instruction 5 \
    --output_dir "data/processed"
```

#### b) Create Judge-Based Dataset

```bash
python scripts/create_judge_dataset.py \
    --model "meta-llama/Llama-3.2-1B-chat" \
    --responses_dir "data/processed" \
    --output_dir "data/judge_dataset"
```

#### c) Create PairRM-Based Dataset

```bash
python scripts/create_pairm_dataset.py \
    --responses_dir "data/processed" \
    --output_dir "data/pairm_dataset"
```

### 2. Model Training

#### a) Train Judge-Based DPO Model

```bash
python scripts/train_dpo_judge.py \
    --model "meta-llama/Llama-3.2-1B-chat" \
    --dataset "data/judge_dataset" \
    --output_dir "models/lora_adapter_judge" \
    --learning_rate 5e-5 \
    --batch_size 8 \
    --num_epochs 3
```

#### b) Train PairRM-Based DPO Model

```bash
python scripts/train_dpo_pairm.py \
    --model "meta-llama/Llama-3.2-1B-chat" \
    --dataset "data/pairm_dataset" \
    --output_dir "models/lora_adapter_pair" \
    --learning_rate 5e-5 \
    --batch_size 8 \
    --num_epochs 3
```

### 3. Model Evaluation

```bash
python scripts/evaluate_models.py \
    --base_model "meta-llama/Llama-3.2-1B-chat" \
    --judge_adapter "models/lora_adapter_judge" \
    --pair_adapter "models/lora_adapter_pair" \
    --test_instructions "data/test_instructions.json" \
    --output_file "evaluation_results.csv"
```

## 📚 Datasets

The project uses the Lima dataset from HuggingFace as the source of instructions. The generated preference datasets are available at:

- Judge-Based Dataset: [HuggingFace Link](https://huggingface.co/xiaokeliu/lora_adapter_judge_based)
- PairRM-Based Dataset: [HuggingFace Link](https://huggingface.co/xiaokeliu/lora_adapter_pair_based)

## 🤖 Models

The trained LoRA adapters are available at:

- Judge-Based DPO Model: [HuggingFace Link](https://huggingface.co/datasets/xiaokeliu/judge_based_data)
- PairRM-Based DPO Model: [HuggingFace Link](https://huggingface.co/datasets/xiaokeliu/pairRM_data)

## 📈 Results

Our comparative analysis shows significant improvements in response quality across both fine-tuned models compared to the base Llama-3.2 model. Key findings include:

- Both DPO models show improved response coherence and instruction following
- The PairRM-based model excels at factual accuracy
- The Judge-based model demonstrates stronger reasoning capabilities
- Iterative DPO training shows compounding improvements in model performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Hu Liu - liu.hu1@northeastern.edu

Northeastern University, MSIS

## 🙏 Acknowledgements

- [HuggingFace](https://huggingface.co/) for hosting datasets and models
- [GAIR/Lima](https://huggingface.co/datasets/GAIR/lima) for the instruction dataset
- [Meta AI](https://ai.meta.com/) for the Llama models
- [PairRM](https://github.com/microsoft/PairRM) for the preference learning algorithm
- [DPO Paper](https://arxiv.org/abs/2305.18290) for the Direct Preference Optimization method
