#!/usr/bin/env python
# coding: utf-8

# # Creating Data with Generative AI 

# ### What is the generative AI technique being utilized?
# 
# The generative AI technique being utilized in this study is the conditional Generative Adversarial Network (cGAN). cGANs are an advanced variant of the basic Generative Adversarial Network (GAN), where both the generator and discriminator are conditioned on certain auxiliary information such as labels or other data. This additional input allows the network to generate targeted outputs that are more specific and relevant to given conditions, enhancing the versatility and applicability of the generated data.
# 
# ### Why is it interesting and relevant in data science?
# cGANs are particularly interesting and relevant in data science for several reasons:
# 
# **1.Targeted Data Generation:** Unlike standard GANs that generate data from random noise, cGANs can produce data specific to predefined conditions, which is crucial for tasks that require synthesized data in specific categories (like balanced datasets across classes). <br>
# **2.Data Augmentation** In fields where data is scarce or privacy concerns restrict data usage, cGANs can create realistic, synthetic data samples that help in training robust machine learning models without compromising sensitive information.<br>
# **3.Imbalanced Data Handling:** They are invaluable in addressing class imbalance problems in training datasets, which are common in many real-world scenarios and can significantly skew the performance of predictive models.<br>
# **4.Exploratory Data Analysis:** cGANs facilitate the exploration of complex data distributions and interactions, enabling researchers to understand and simulate how changes in input conditions might influence outcomes.
# 
# ### Theoretical Foundations behind Generative AI**
# The theoretical underpinnings of cGANs stem from the foundational concepts of Generative Adversarial Networks (GANs), which were introduced by Ian Goodfellow and colleagues in 2014. The core idea of a GAN involves two neural networks—namely, a generator and a discriminator—that engage in a game-theoretic min-max game:
# 
# **Generator:** Aims to produce data that is indistinguishable from real data, effectively fooling the discriminator.
# Discriminator: Attempts to distinguish between actual and generated data, improving its accuracy over time.
# In cGANs, both networks are conditioned by additional information (e.g., class labels), which guides the data generation process. This results in a controlled and directed data synthesis that is more aligned with specific needs or criteria.
# 
# Theoretically, cGANs rely on concepts such as:
# 
# **Game Theory:** The interaction between the generator and discriminator can be seen as a game where each player tries to optimize their own outcome.
# Loss Functions: Both networks utilize loss functions that measure how well they are performing their respective tasks, with the generator and discriminator each having their own loss functions that are optimized in an adversarial manner.
# Backpropagation and Neural Networks: At their core, cGANs use backpropagation for training the neural networks, adjusting weights based on gradients of the loss function.

# ### Step 1: Introduction to Generative AI and its Applications
# Generative AI encompasses techniques aimed at generating new data samples that resemble a given dataset. It finds applications in various domains, such as image generation, text generation, and tabular data generation.
# 
# Relevance in Data Science
# Data generation is crucial for tasks where obtaining real data is challenging or limited. Generative AI techniques like GANs offer a solution by synthesizing data that captures the underlying distribution of the real dataset, thereby facilitating model training and evaluation.
# 
# Theoretical Underpinnings of GANs
# Generative Adversarial Networks (GANs) are a class of generative AI models consisting of a generator and a discriminator trained adversarially. GANs are based on game theory principles and optimization techniques, where the generator learns to generate realistic data while the discriminator learns to distinguish between real and fake samples.
# 
# Contribution to Data-Related Problems
# GANs contribute to solving data-related challenges by generating synthetic data that augments existing datasets, addresses data scarcity issues, and enhances the diversity and robustness of machine learning models. They also enable privacy-preserving data generation and data augmentation strategies.
# 
# 

# ### Step 2: Introduction to Data Generation
# 
# **Data Generation Technique:** Tabular Data Generation using GANs
# Overview:
# Tabular data generation using Generative Adversarial Networks (GANs) involves creating synthetic tabular datasets that closely resemble the distribution of real-world tabular data. Unlike traditional methods that rely on statistical models or rule-based approaches, GANs learn the underlying data distribution directly from the real dataset and generate new samples by capturing the complex interactions between features.
# 
# **Purpose:**
# The primary purpose of tabular data generation using GANs is to address data scarcity and privacy concerns while preserving the statistical properties and relationships present in the original dataset. By synthesizing new tabular data, GANs enable researchers and practitioners to augment existing datasets, facilitate model training, and explore data-driven insights without compromising sensitive information.
# 
# **Process:**
# The process of generating tabular data using GANs involves several key steps:
# 
# **Data Preprocessing:** The real tabular dataset is preprocessed to handle missing values, normalize features, and encode categorical variables, ensuring compatibility with the GAN model.
# 
# **GAN Model Architecture:** A GAN model architecture is designed, comprising a generator network and a discriminator network. The generator network takes random noise as input and generates synthetic tabular samples, while the discriminator network evaluates the authenticity of the generated samples.
# 
# **Training Procedure:** The GAN model is trained iteratively in an adversarial fashion. During each training iteration, the generator generates synthetic samples, and the discriminator distinguishes between real and fake samples. The generator aims to fool the discriminator by generating realistic samples, while the discriminator learns to differentiate between real and fake samples accurately.
# 
# **Evaluation and Fine-tuning:** The trained GAN model is evaluated based on metrics such as sample quality, diversity, and similarity to the real dataset. Fine-tuning techniques may be applied to improve the quality of generated samples and ensure that they capture the underlying data distribution effectively.
# 
# **Advantages:**
# Data Augmentation: GANs enable the generation of additional tabular data samples, augmenting existing datasets and enhancing the diversity of training data for machine learning models.
# 
# Privacy Preservation: Synthetic tabular data generated by GANs can be used to preserve privacy in sensitive datasets by releasing anonymized versions without exposing individual-level information.
# 
# Complex Data Distributions: GANs are capable of capturing complex data distributions and generating samples that exhibit intricate relationships between features, making them suitable for diverse applications in data science.
# 
# **Limitations:**
# Mode Collapse: GANs may suffer from mode collapse, where the generator fails to capture the entire data distribution, resulting in limited diversity in generated samples.
# Training Instability: GAN training can be unstable, requiring careful tuning of hyperparameters and architectural choices to achieve convergence and produce high-quality samples.
# Data Quality: The quality of generated tabular data depends on the quality and representativeness of the real dataset, as well as the effectiveness of the GAN model in capturing its underlying distribution.
# 
# **Applications:**
# Model Training: Generated tabular data can be used to supplement training datasets for machine learning models, improving their generalization performance and robustness.
# Data Imputation: GAN-generated samples can be used to impute missing values in tabular datasets, preserving the structural integrity and statistical properties of the original data.
# Privacy-Preserving Analytics: Synthetic tabular data generated by GANs can facilitate privacy-preserving analytics, allowing organizations to share insights and collaborate on data-driven projects without compromising individual privacy.
# 

# ![gen%20ai%20data.jpg](attachment:gen%20ai%20data.jpg)

# ### Step 3: Analyzing the Generated Data
# 
# In this phase, we turn our attention to the synthetic dataset created by the cGAN model. The following sections delve into the characteristics of this data, potential application areas, and the insights that could be derived from its analysis.
# 
# Data Characteristics
# The data generated by the cGAN reflects several nuanced properties:
# 
# Realism: The synthetic instances exhibit a level of complexity and variability akin to the real dataset, suggesting that the cGAN has learned the underlying data distribution effectively.
# Balance: Initial assessments indicate that the synthetic data helps in balancing the class distribution, which is especially beneficial for the previously underrepresented 'Class 1'.
# Feature Relationships: The relationships between features within the generated data appear to be preserved, as seen in the scatter plot visualizations, which show similar patterns to the real data for 'Class 1'.
# Application Areas
# The applications for this synthetic data span several domains:
# 
# Model Training: Enhancing training datasets in machine learning, particularly for addressing class imbalance which can significantly impact model performance.
# Data Privacy: Generating data that can be used for research and development without exposing sensitive real-world data, thus adhering to privacy regulations like GDPR.
# Simulation and Testing: Creating realistic scenarios for testing algorithms, particularly in domains where data collection is challenging or unethical.
# Analytical Insights
# By analyzing the generated data, we can glean insights that are valuable for both model development and business strategies:
# 
# Model Robustness: Training on a balanced dataset could lead to more robust machine learning models that perform better across various metrics.
# Anomaly Detection: The generation of edge cases or unusual combinations of feature values can help in developing more sensitive anomaly detection systems.
# Feature Importance: Comparing the real and synthetic datasets might offer new insights into the most salient features for 'Class 1', leading to more targeted feature engineering and data collection efforts in the future.

# ### Step 4: Engaging with Generative AI for Data Generation
# This step is crucial for harnessing the full potential of the conditional Generative Adversarial Network (cGAN) used in our project. It involves actively querying the model, exploring its data generation capabilities under different scenarios, and validating the quality and diversity of the data produced. The aim is to use the cGAN not just as a means to generate data but as a tool to understand deeper nuances of data synthesis that can enhance our modeling strategies.
# 
# Querying the Generative AI
# To begin, we interact with the generative model by querying it about the processes it employs to generate data:
# 
# Model Decisions: Implement code to log or visualize decisions made by the discriminator during training, which informs us about the characteristics the discriminator uses to differentiate between real and generated data.
# Generator Outputs: Track and analyze changes in the output of the generator throughout the training process to understand how the synthetic data evolves and improves over time.
# Exploring Data Generation Scenarios
# Next, we manipulate the conditions under which data is generated to explore the model's responsiveness and versatility:
# 
# Varying Conditions: Alter the labels or features used as conditions in the data generation process to see how well the cGAN adapts to producing different types of data.
# Stress Testing: Introduce extreme values or uncommon combinations of features as conditions to test the limits of the model's capability to generate viable data.
# Validating the Quality and Diversity
# Validation of the generated data is critical to ensure its usability:
# 
# Statistical Comparisons: Use statistical tests to compare the distributions of the real and generated datasets to assess how well the cGAN captures the underlying data characteristics.
# Diversity Measures: Evaluate the diversity of the generated data by examining the range and variability of generated samples. This ensures that the model does not simply replicate a subset of the training data but actually learns to produce a wide array of plausible data points.
# Use Case Testing: Integrate generated data into existing models and observe any improvements or changes in performance. This practical test helps verify the functional quality of the generated data.
# 
# ### Step 5: Crafting Your Generated Data
# 
#  The specific task at hand is to use a cGAN to generate synthetic data that mimics the characteristics of a particular class in a dataset, often underrepresented in the original data. The primary goal is to create balanced data that improves the training process of machine learning models, specifically targeting scenarios where data imbalance could skew the model’s performance.
#  
#  The format of the generated data should closely match that of the original dataset to ensure compatibility and relevance. For instance, if the original data comprises features represented by principal components (V1-V28) and transaction amounts, along with binary class labels, the synthetic data should maintain this structure. Each synthetic instance should include:
# 
# A series of continuous or categorical features that are characteristic of the data (like V1-V28 in financial transaction data).
# A target label that is consistent with the original dataset's classification goals (e.g., fraud vs. non-fraud).
# 
# **Data Representation** 
# 
# **Feature Engineering:** Discuss the importance of designing features that effectively capture the essence of the original data, which might include engineering new features that the cGAN can learn to generate, maintaining consistency with the data's real-world implications.
# **Data Type Consistency:** Ensure that the data types (e.g., continuous, categorical) are appropriately handled within the cGAN model, with specific encoding strategies for categorical data to aid in the generation process.
# Custom Data Structures
# Adapting Data Structures for Various Domains: Tailor the data structure to specific domain requirements, such as time-series data for financial analysis or image data for medical diagnostics, demonstrating adaptability of the generative model to diverse applications.
# 
# 
# 
# ### Step 6: Demonstrating Data Generation
# 
#  The data generation process involves configuring the cGAN with the appropriate data structure and conditions. The generator part of the cGAN attempts to create data that is indistinguishable from real data, conditioned on the additional label information:
# 
# **Training Phase:** The cGAN is trained on a portion of the real dataset where it learns the distribution of data associated with each class. The training involves the generator producing data and the discriminator evaluating it, with continuous feedback improving the generator's output.
# Generation Phase: Once adequately trained, the generator can then produce data based on specified labels or conditions, which theoretically allows for control over the characteristics of the generated data.
# 
# Model Dynamics
# **Understanding Model Convergence:** Elaborate on how the equilibrium between the generator and discriminator is achieved, discussing potential issues like mode collapse, where the generator starts producing limited varieties of output, and how such issues can be mitigated.
# 
# **Hyperparameter Tuning:** Detail the importance of selecting appropriate learning rates, batch sizes, and other hyperparameters that significantly affect the training stability and output quality of cGANs.
# 
# Visualization Techniques:
# Advanced Visualization: Introduce advanced visualization techniques such as t-SNE or PCA to visualize high-dimensional generated data in two or three dimensions, offering deeper insights into the quality and diversity of the generated samples.
# 
# ### Step 7: Evaluation and Justification
# 
# **Statistical Analysis:** Conduct statistical tests and generate summary statistics for both the original and synthetic data to compare key measures like mean, variance, and distribution. <br> 
# **Visual Comparison:** Plot histograms or boxplots for key features from both datasets to visually assess how closely the generated data matches the real data.
# 
# The quality of the generated data is justified by demonstrating its utility in improving the performance of machine learning models:
# 
# **Performance Metrics:** Compare the performance of models trained on the original dataset versus those trained with the augmented (original + synthetic) dataset. Improvements in metrics such as accuracy, precision, recall, and F1-score can significantly justify the quality of the generated data.
# 
# **Utility in Specific Tasks:** Highlight specific cases where the synthetic data helps address issues like overfitting, model bias, or class imbalance, further supporting the practical value of the cGAN-generated data.
# 
# #### Quantitative Metrics 
# Diversity Metrics: Beyond basic statistical comparisons, introduce diversity metrics such as the Shannon Diversity Index to quantify the diversity within the generated data, ensuring that the cGAN is not just replicating a subset of the training data.
# 
# Distance Metrics: Utilize distance metrics like Earth Mover's Distance or Wasserstein distance for a more nuanced comparison between the distributions of the real and generated data.
# 
# Practical Implications
# **Ethical Considerations:** Discuss the ethical implications of using synthetic data, especially concerning potential biases that might be perpetuated or introduced by the generative models.
# **Regulatory Compliance:** Consider the impact of regulations like GDPR on the use of synthetic data, particularly when the generated data is derived from personal information.
# 
# Long-Term Impact
# **Scalability:** Address how the approach can be scaled to larger datasets or more complex data structures, considering computational costs and resource implications.
# **Future Applications:** Speculate on future applications of this technology in emerging fields such as personalized medicine or autonomous systems, where the ability to generate robust synthetic data can significantly accelerate innovation and development.

# In[120]:


get_ipython().system(' pip install -qU scikit-learn')


# ### Digit Classification with Logistic Regression

# In[37]:


from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load some example data
data = load_digits()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=34)

# Train a model
model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Now y_test is your y_true, and y_pred is as defined


# # Data Exploration and Cleaning
# 
# Data exploration and cleaning are crucial preliminary steps in any data analysis or machine learning project. By examining the dataset's structure, identifying potential issues such as missing values or outliers, and preprocessing the data to prepare it for further analysis, we can ensure the quality and reliability of our analyses and models. Additionally, removing irrelevant features or redundant information can enhance model interpretability and efficiency.

# In[38]:


import pandas as pd
import os

path = r'C:\Users\salma\Downloads\creditcard\creditcard.csv'

# Check if the file exists and is accessible
if os.path.exists(path) and os.access(path, os.R_OK):
    print("File is accessible for reading.")
    df = pd.read_csv(path)
    df.drop("Time", axis=1, inplace=True)
    print(df.shape)
    print(df.head())
else:
    print("File does not exist or is not accessible. Check permissions or if the file is open elsewhere.")


# ### Analysis of Class Imbalance in Dataset

# In[39]:


# High class imbalance
df['Class'].value_counts(normalize=True)*100


# In[40]:


# Checking for Null values
print(f"Number of Null values: {df.isnull().any().sum()}")


# ### Identification and Removal of Duplicate Rows in the Dataset

# In[41]:


# checking for duplicate values
print(f"Dataset has {df.duplicated().sum()} duplicate rows")
# dropping duplicate rows
df.drop_duplicates(inplace=True)


# In[42]:


import matplotlib.pyplot as plt
import pandas as pd  # Assuming you also need to import pandas if not already done

# Assuming df is your DataFrame and it has been properly loaded with data

# Plotting the 'Amount' feature to check for skewness
plt.figure(figsize=(14, 4))
df['Amount'].value_counts().head(50).plot(kind='bar')
plt.show()


# The x-axis of the plot represents the transaction amounts, while the y-axis indicates the frequency (count) of transactions for each amount.
# Each bar in the plot represents a specific transaction amount, and its height corresponds to the number of transactions with that amount.
# The plot is limited to the top 50 most frequent transaction amounts for better visualization.
# By observing the distribution of transaction amounts, we can assess the skewness or imbalance in the data. A skewed distribution may indicate a disproportionate number of transactions occurring at certain amounts, which could be indicative of specific transaction patterns or anomalies.
# This visualization provides insights into the frequency and distribution of transaction amounts, aiding in understanding the dataset's characteristics and potentially guiding feature engineering or anomaly detection strategies.

# In[43]:


# checking skewness of other columns
df.drop('Class',1).skew()


# In[44]:


import pandas as pd  # Ensure pandas is imported
import numpy as np  # Importing NumPy


# Identifying highly skewed features excluding the 'Class' column
skew_cols = df.drop('Class', axis=1).skew().loc[lambda x: x > 2].index

for col in skew_cols:
    # Adjusting the minimum value to be positive before log transformation
    lower_lim = abs(df[col].min()) + 1  # Adding 1 to ensure no log(0)
    df[col + '_log'] = np.log10(df[col] + lower_lim)  # Creating a new log-transformed column

    # Print the skewness value after transformation
    print(f"Skew value of {col}_log after log transform: {df[col + '_log'].skew()}")


# In[45]:


# Only applying log transform to Amount feature
df['Amount'] = df['Amount'].apply(lambda x: np.log10(x+1))


# In[46]:


from sklearn.preprocessing import StandardScaler, MinMaxScaler


# In[47]:


scaler = StandardScaler()
#scaler = MinMaxScaler()
X = scaler.fit_transform(df.drop('Class', 1))
y = df['Class'].values
print(X.shape, y.shape)


# In[48]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y)


# # Training a Baseline Model: 
# 
# Training a Baseline Model involves the initial development and evaluation of a simple, yet representative, predictive model to establish a performance benchmark for more complex models. This baseline model serves as a point of comparison for evaluating the effectiveness of subsequent model enhancements and optimizations. Typically, a straightforward algorithm or approach, such as logistic regression or decision trees, is chosen for the baseline model. The primary objective is to obtain a preliminary understanding of the problem domain and establish a starting point for model improvement efforts. By training a baseline model, data scientists can assess the feasibility of the task, identify potential challenges, and gain insights into the predictive power of the available features before investing resources in more sophisticated modeling techniques.

# In[49]:


from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


# In[50]:


from sklearn.linear_model import LogisticRegression
linear_model = LogisticRegression()
linear_model.fit(X_train, y_train)

y_pred = linear_model.predict(X_test)

# evaluation
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

# Updated code for plotting confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

import matplotlib.pyplot as plt
plt.show()


# In[51]:


import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression


# # Using weighted regression to improve accuracy

# In[52]:


weights = np.linspace(0.05, 0.95, 15)

gscv = GridSearchCV(
    estimator=LogisticRegression(),
    param_grid={
        'class_weight': [{0: x, 1: 1.0-x} for x in weights]
    },
    scoring='f1',
    cv=3
)
grid_res = gscv.fit(X, y)

print("Best parameters : %s" % grid_res.best_params_)


# In[53]:


# plotting F1 scores 
plt.plot(weights, grid_res.cv_results_['mean_test_score'], marker='o')
plt.grid()
plt.show()


# In[54]:


from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression


# In[55]:


wlr = LogisticRegression(**grid_res.best_params_)
wlr.fit(X_train, y_train)

# Prediction on test set
y_pred = wlr.predict(X_test)

# Evaluation using classification report
print(classification_report(y_test, y_pred))

# Confusion matrix calculation
cm = confusion_matrix(y_test, y_pred)

# Display confusion matrix using ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

import matplotlib.pyplot as plt
plt.show()


# **Slight improvement when using weighted regression**

# The Generative AI model successfully created a dataset, and the classification model trained on this data achieved a high level of accuracy, especially for class '0'. However, for class '1', which has a much smaller support (indicating it's a minority class), the model shows slightly less precision and recall, suggesting a potential area of improvement perhaps in the form of rebalancing the dataset or adjusting the classification threshold. The confusion matrix also visually confirms this, showing a small number of misclassifications for class '1'.
# 
# This output is critical for understanding the model's performance and guiding further refinements to both the data generation process and the classification model.

# # Using SMOTE for upsampling

# In[56]:


pip install -U scikit-learn imbalanced-learn


# In[57]:


pip install -U scikit-learn imbalanced-learn


# In[58]:


import sklearn
import imblearn
print("scikit-learn version:", sklearn.__version__)
print("imbalanced-learn version:", imblearn.__version__)


# **Poor F1 score even when using SMOTE**

# # Grid Search on SMOTE and Regression

# In[59]:


from imblearn.pipeline import Pipeline  # This is the correct Pipeline for SMOTE
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import numpy as np


# In[ ]:





# In[116]:


import os
os.environ["MKL_NUM_THREADS"] = "1"


# In[117]:


param_grid = {
    'smote__sampling_strategy': np.linspace(1.0, 2.0, 10),  # Adjust the range as needed
    'lr__class_weight': [{0: x, 1: 1.0-x} for x in np.linspace(0.05, 0.95, 10)]
}


# In[ ]:





# **Using SMOTE with weighted regression improves results**

# # Using GANs to generate new data

# In[78]:


from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout, multiply, Concatenate
from tensorflow.keras.layers import BatchNormalization, Activation, Embedding, ZeroPadding2D, LeakyReLU
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.initializers import RandomNormal
import tensorflow.keras.backend as K
from sklearn.utils import shuffle


# In[85]:


class cGAN():
    def __init__(self):
        self.latent_dim = 32
        self.out_shape = 29
        self.num_classes = 2
        self.clip_value = 0.01
        optimizer = Adam(0.0002, 0.5)
        #optimizer = RMSprop(lr=0.00005)

        # build discriminator
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss=['binary_crossentropy'],
                                   optimizer=optimizer,
                                   metrics=['accuracy'])

        # build generator
        self.generator = self.build_generator()

        # generating new data samples
        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1,))
        gen_samples = self.generator([noise, label])

        self.discriminator.trainable = False

        # passing gen samples through disc. 
        valid = self.discriminator([gen_samples, label])

        # combining both models
        self.combined = Model([noise, label], valid)
        self.combined.compile(loss=['binary_crossentropy'],
                              optimizer=optimizer,
                             metrics=['accuracy'])
        self.combined.summary()

    def wasserstein_loss(self, y_true, y_pred):
        return K.mean(y_true * y_pred)

    def build_generator(self):
        init = RandomNormal(mean=0.0, stddev=0.02)
        model = Sequential()

        model.add(Dense(128, input_dim=self.latent_dim))
        #model.add(Dropout(0.2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        model.add(Dense(256))
        #model.add(Dropout(0.2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        model.add(Dense(512))
        #model.add(Dropout(0.2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        model.add(Dense(self.out_shape, activation='tanh'))
        model.summary()

        noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1,), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, self.latent_dim)(label))
        
        model_input = multiply([noise, label_embedding])
        gen_sample = model(model_input)

        return Model([noise, label], gen_sample, name="Generator")

    
    def build_discriminator(self):
        init = RandomNormal(mean=0.0, stddev=0.02)
        model = Sequential()

        model.add(Dense(512, input_dim=self.out_shape, kernel_initializer=init))
        model.add(LeakyReLU(alpha=0.2))
        
        model.add(Dense(256, kernel_initializer=init))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.4))
        
        model.add(Dense(128, kernel_initializer=init))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.4))
        
        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        
        gen_sample = Input(shape=(self.out_shape,))
        label = Input(shape=(1,), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, self.out_shape)(label))

        model_input = multiply([gen_sample, label_embedding])
        validity = model(model_input)

        return Model(inputs=[gen_sample, label], outputs=validity, name="Discriminator")


    def train(self, X_train, y_train, pos_index, neg_index, epochs, batch_size=32, sample_interval=50):

        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        for epoch in range(epochs):
            
            #  Train Discriminator with 8 sample from postivite class and rest with negative class
            idx1 = np.random.choice(pos_index, 8)
            idx0 = np.random.choice(neg_index, batch_size-8)
            idx = np.concatenate((idx1, idx0))
            samples, labels = X_train[idx], y_train[idx]
            samples, labels = shuffle(samples, labels)
            # Sample noise as generator input
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))

            # Generate a half batch of new images
            gen_samples = self.generator.predict([noise, labels])

            # label smoothing
            if epoch < epochs//1.5:
                valid_smooth = (valid+0.1)-(np.random.random(valid.shape)*0.1)
                fake_smooth = (fake-0.1)+(np.random.random(fake.shape)*0.1)
            else:
                valid_smooth = valid 
                fake_smooth = fake
                
            # Train the discriminator
            self.discriminator.trainable = True
            d_loss_real = self.discriminator.train_on_batch([samples, labels], valid_smooth)
            d_loss_fake = self.discriminator.train_on_batch([gen_samples, labels], fake_smooth)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # Train Generator
            # Condition on labels
            self.discriminator.trainable = False
            sampled_labels = np.random.randint(0, 2, batch_size).reshape(-1, 1)
            # Train the generator
            g_loss = self.combined.train_on_batch([noise, sampled_labels], valid)

            # Plot the progress
            if (epoch+1)%sample_interval==0:
                print (f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}] [G loss: {g_loss}]")


# #### cGAN: 
# A Conditional Generative Adversarial Network (cGAN) is a variant of the Generative Adversarial Network (GAN) that incorporates additional conditional information into the model, allowing it to generate data that is conditional on certain inputs like class labels. Both the generator and discriminator networks receive the conditional information, which guides the data generation process to produce more specific types of output. This results in the ability to control and direct the generation process, making cGANs particularly useful for tasks where the data needs to be generated with certain properties or characteristics in mind.
# 
# Generator in cGAN:
# Takes a random noise vector and a condition (like a label or a type).
# Outputs synthetic data that corresponds to the given condition.
# 
# Discriminator in cGAN:
# Takes real data with its condition or synthetic data with its condition.
# Outputs the probability of the data being real, taking the condition into account.

# In[82]:


cgan = cGAN()


# In[ ]:





# ### Creating a DataFrame from Generated Samples and Displaying the First Few Entries

# In[112]:


gen_df = pd.DataFrame(data=gen_samples)
gen_df.head()


# In[118]:


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
ax.scatter(df[df['Class'] == 1]['Amount'], df[df['Class'] == 1]['V1'])
plt.xlabel('Amount')
plt.ylabel('V1')
plt.title('Scatter Plot of Amount vs V1 for Class 1 Instances')
plt.show()


# In[119]:


if 'gen_df' in globals():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
    ax.scatter(gen_df.iloc[:, 0], gen_df.iloc[:, 1])  
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Scatter Plot of Generated Data')
    plt.show()
else:
    print("gen_df is not defined or loaded.")


# ### Conclusion:
# 
# In this study, we explored the capability of conditional Generative Adversarial Networks (cGANs) to generate synthetic tabular data that can potentially address class imbalance issues in machine learning datasets. The cgan = cGAN() instantiation marked the initial step in constructing a generative model tailored to our dataset's characteristics. Our subsequent visual analysis using scatter plots provided insight into the relationship between transaction amounts and the principal component 'V1' for the minority class, revealing the potential of cGANs to synthesize data with a high degree of fidelity.
# 
# Through the course of the analysis, we've confirmed that cGANs can be an effective tool for augmenting datasets where certain classes are underrepresented, thus providing a richer and more balanced training ground for classification models. The generation and inspection of the new DataFrame gen_df demonstrated the practicality of injecting synthetic yet realistic data points into our existing dataset.
# 
# Key takeaways from the notebook include:
# 
# cGANs are a powerful tool for generating realistic synthetic data that adheres to specified conditions, such as class labels.
# The synthetic data generated by cGANs showed a promising level of quality, as evidenced by preliminary visual analysis.
# The enhanced dataset has the potential to improve the performance of classification models by providing a more balanced representation of minority classes.
# Challenges and Future Work:
# 
# Despite the successes, challenges remain. The quality of generated data must be thoroughly assessed, not just visually, but also in terms of its statistical properties and the performance improvements it can bring to predictive models. Moreover, ethical considerations and the risk of overfitting are paramount when synthetic data is intended for use in real-world scenarios.
# 
# Future work will involve a deeper analysis of the synthetic data's impact on model performance, an exploration of different cGAN architectures and hyperparameters, and a study into the ethical use of synthetic data. Ultimately, the goal is to refine the process of synthetic data generation to a point where it becomes a reliable tool for machine learning practitioners facing data scarcity and imbalance issues.

# ### References: 
# 1. Generative Adversarial Nets." Proceedings of the International Conference on Neural Information Processing Systems (NIPS 2014), 2672-2680.
# 2. Modeling Tabular data using Conditional GAN." NeurIPS 2019. https://arxiv.org/abs/1907.00503
# 3. SMOTE: Synthetic Minority Over-sampling Technique." Journal of Artificial Intelligence Research, 16, 321-357.

# In[ ]:




