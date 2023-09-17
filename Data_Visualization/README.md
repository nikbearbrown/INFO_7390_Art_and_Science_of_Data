# Data Visualization


 
## Data Visualization Recipe 

### Any code and notebooks related to the lessons will be found in this directory.  

Types of Visualization (The Why?)
* Explanatory (Communicate something to a larger audience)

  Primarily used to communicate intricate patterns or findings to a larger audience. This type of visualization streamlines complex data, transforming it into easily digestible visuals that resonate with the audience's understanding.
* Exploratory (Find out interesting aspects/patterns in the data)

  Aimed at uncovering hidden patterns, relationships, and trends within the data. This is instrumental for data scientists and analysts during the initial phases of data analysis when they are trying to gain insights and generate hypotheses.
* Confirmatory (Visual evidence for an assertion/hypothesis)

  Offers a visual means to provide evidence in support of a specific assertion or hypothesis. It ensures that the conclusions drawn are based on factual evidence represented in the visualization.

Check the data! GIGO (Garbage-in, garbage-out):  It's crucial to ensure data quality before diving into visualization. Feeding flawed or irrelevant data will result in misleading visuals, hence the term "garbage in, garbage out."
* Missing values?: Ensure that there aren't significant gaps in your dataset that might skew results. Tools and techniques for data imputation can help address this.
* Data Imputation : Data Imputation refers to the procedure of using alternate values in place of missing data. It is also referred to as unit imputation.
    * Missing information can produce a significant degree of bias that makes analyzing and processing data more difficult and reduces the efficiency.
 * Importance of data imputation : Distorts datasets : Large number of missing data can lead to anomalies in the variable distribution,which can change the relative importance of different categories in the dataset.
     * Impacts the final model : Missing data leads to the bias in the dataset, which could affect the final model analysis.
     * Difficult to work with majority machine learning libraries : When utilizing machine learning libraries, mistakes may occur because there is no automatic handling of the missing data.
* Data Imputation Techniques : There are different data imputation technique some of the technique are :
    * K Nearest Neighbour : The objective is to find K nearest examples in the data where the value in the relevant feature is not absent and then substitute the value of the feature that occurs most frequently in the group.
    * Missing Value Prediction : Using a machine learning module to determine the final imputation value for charactersitic based on other features. The model is trained using the values in the remaining columns, and the rows in feature without missing values.
    * Most Frequent Value : In this method the most frequent column is used to replace the missing values.
*Challenges in Data Imputation Techniques :Missing Data Mechanism: Understanding the missing data mechanism is crucial. Is the data missing completely at random (MCAR), missing at random (MAR), or not missing at random (NMAR)? The mechanism can affect the choice of imputation method.
* Bias: Imputing missing values can introduce bias if not done carefully. The imputed values should resemble the true underlying distribution as closely as possible to avoid distorting the data.
* Imputation Quality Assessment: It's important to assess the quality of imputed values. Some metrics, like root mean squared error (RMSE) or mean absolute error (MAE), can be used to evaluate imputation performance.
* Handling Categorical Data: Imputing categorical data can be tricky. Techniques like using the mode or more advanced approaches like random forest imputation can be employed.
* Time-Series Data: For time-series data, imputation methods need to account for temporal dependencies. Techniques like forward fill, backward fill, or interpolation with consideration of time can be useful.
* Data Scale: Scaling issues can arise in imputation. For example, imputing missing values for variables with different scales (e.g., age and salary) may require normalization or standardization. 
* Data types : Understanding the nature of your data is pivotal.
  - There are several reasons why understanding the nature of data is important as its the first step in any data analysis-
    1. Data Cleaning: Data in the real world is often messy and inconsistent. Understanding your data can help you identify errors or anomalies that need to be addressed before analysis. ex- if certain columns need to contain a specifc data type such as Int but you see some string values, this would indicate a problem.
    2. Predictive Modeling: If you’re building a predictive model, understanding your data can inform feature engineering and the choice of model. ex- categorical variables might need to be one-hot encoded before being used by any ML model as its efficient to predict using binary digits rather than a string of characters.
    3. Effective Communication: Different types of data require different types of visualizations. ex- categorical data might be best represented by a bar chart, while continuous data might be better suited for a histogram or scatter plot.
   
  - Few common data types and its uses:
  
    * Categorical, Nominal, Ordinal: Classifications without a particular order or with a hierarchy.
      1. Categorical - This type of data is used to label data in a dataset into a finite number of discrete groups. Categorical data might not have a logical order. ex- gender (Male, Female, Other) is a categorical variable.
      2. Nominal - Nominal data is a type of categorical data where the categories do not have a standard hierarchy such as colors (red, blue, green) or city names (Boston, San Francisco).
      3. Ordinal - Ordinal data is also categorical but with a clear ordering or hierarchy such as customer satisfaction ratings (Unsatisfied, Neutral, Satisfied) are ordinal.
    * Numeric: Quantifiable data that can be measured. Types of Numeric data:
      1. Discrete: These are whole numbers and represent countable data. ex- the number of employees in a company.
      2. Continuous: These can take any value within a range and represent measurable quantities. ex- temperature or weight.
    * Strings & Dates: Textual data and specific time points or durations.
      1. String: represent textual data and can include names, addresses, and descriptions.
      2. Dates: represent specific points in time and can be used to analyze trends over time.
    * Boolean: This type of data represents truth values and is commonly used in logic operations. It can only take two values: True or False.
    * Interval: Interval data is numeric but with a consistent scale and not necessarily start with zero (like temperature in Celsius or Fahrenheit).
    * Ratio: Ratio data is numeric with a consistent scale and does indeed start with zero (like height, weight, age).

      
* Descriptive statistics: A preliminary overview of data.
    * Numeric: Using methods like .describe() to get count, mean, standard deviation, etc.
    * Categorical: Evaluate using Shannon entropy to measure unpredictability, count unique values, and ascertain the frequency of each value.
* Data type attributes (GPS, Sequence/Time-series, Nodes/Edges) - User feedback

  It's essential to understand the context.
    * GPS: Geographical points
    * Sequence/Time-series: Data points arranged in time order
    * Nodes/Edges: Data points representing network connections, needing feedback from users to interpret significance.

* Data structure (Tabular, Graph, Time-series, Hierarchical, Geographic, Map, Network, etc.) - User feedback

  Knowing the structure helps in selecting the right visualization.
    * Tabular, Graph, Time-series, Hierarchical, Geographic, Map, Network, etc. Each offers different insights and requires unique visualization techniques.
* Data type semantics (Spatial, Temporal) - User feedback

  Semantic meaning can influence interpretation.
    * Spatial: Relating to space
    * Temporal: Relating to time
* Outliers? (Numeric Box-whisker x times (deflaut 1.5) interquartile range, categorical would be rare values/low % default < 1%)

  
    Outliers are data points in a dataset that differ significantly from the typical data points. They may show variations in a measurement, faults in the 
    experiment, or a novelty and can be significantly larger or significantly smaller than the other data points. The effects of outliers on statistical analysis 
    can be significant, and they can skew the outcomes of any hypothesis testing. For accurate findings, it is crucial to thoroughly identify any potential 
    outliers in your dataset and deal with them appropriately.

   How do you identify outliers?

   Use of statistical tests like z-scores or interquartile range (IQR) is one of the most used techniques.  We determine the z-score for each data point in the 
   dataset using the z-score method. A data point is regarded as an outlier if the z-score exceeds a predetermined threshold. Any data point with a z-score 
   larger than 3 or less than -3 is regarded as an outlier since the threshold value is often set to 3 or -3.

   In the IQR approach, we first determine the dataset's IQR, which is the difference between the first and third quartiles (Q1 and Q3). Then, based on the IQR, 
   a range of values that are deemed "normal" are established. An outlier is any data point that lies outside of this range.
   
   Through data visualisation, outliers can also be found. We may visually locate any data points that are considerably different from other points in the 
   dataset by showing the data points on a graph.

    These are unusual data points that can heavily influence the overall visualization.
    * Numeric: Use Box-whisker plots to identify values that fall outside the interquartile range.
    * Categorical: Identify rare values or those that occur less frequently.

To do:
* Enough data (Power)?

  * Sample Size: Ensure your dataset is large enough to draw valid conclusions and to represent the population or phenomenon you're studying accurately.
  * Quality of Data: The quality of your data is more important than the quantity. Your data should be accurate, consistent, and up-to-date.
  * Variance and Standard Error: Analyze the variance and standard error to know the reliability of your data. Smaller standard errors indicate more reliable data.
  * Power Analysis: Conduct a power analysis to determine the minimum sample size needed for your analysis to be reliable.
  
* Is the data stationary? <a href='https://www.youtube.com/watch?v=R69TZFNEao4'>See Video</a>   
  * Stationary data is data that exhibits a consistent statistical behavior over time. This kind of data has statistical properties such as mean, variance, and autocorrelation that do not change significantly across different time intervals.
  * This is important to evaluate when analyzing because many statistical methods and models assume stationarity. If the data is not actually stationary, it can be more challenging to analyze and model accurately.
  * Techniques to convert data to stationary data:
     * Differencing:
       * First-Order Differencing: Most commonly used. This involves calculating the difference between consecutive data points.
       * Seasonal Differencing: Used when there is a seasonal component (e.g., data with recurring patterns over a fixed time period). Seasonal differencing involves subtracting the value of the series at the same point in the previous season.
       * Higher-Order Differencing: Used if first-order differencing doesn't make the data stationary. Perform second-order (or higher-order) differencing by applying the differencing operation multiple times.
     * Transformation:
       * Log Transformation: Taking the natural logarithm (or other appropriate transformations like square root or cube root) of the data can stabilize variance and make it more consistent across time, especially if the data exhibits exponential growth.
       * Box-Cox Transformation: The Box-Cox transformation is a family of power transformations that includes the logarithm as a special case. It can be used to find the transformation that best stabilizes the variance and makes the data approximately normal.
       * Other Transformations: Depending on the characteristics of the data, other transformations like taking the inverse or applying a polynomial transformation may be used.
* Is the data biased?


Fix data issues and log what was done
* Impute missing values
  * Type of missing values:<br>
  * Missing completely at Random:<br>
    The missing value has absolutely no relation with other observations.<br>
  * Missing Data not at Random:<br>
      There is a relationship between missing value and other observations.<br>
  * Missing at Random:<br>
      Some values are missing at random.<br>

  **Imputation Techniques**:<br>
  **Mean, median, Mode**:<br>
    **Assumption**: Data is missing completely at random.<br>
      Operation:<br>
      Replacing the NaN with most frequently occurring variable based on mean, median or mode.<br>

  **Random Sample imputation**:<br>
    **Assumption**: Data is missing completely at random.<br>
      Operation:<br>
      Taking random observation from given dataset and replace the NaNs with these observations.<br>

  **End of Distribution**:<br>
    **Assumption**: Data not missing completely at random.<br>
    Operation:<br>
    Replace NaN in the dataset with the values at the extremes (outliers)<br>
    This technique takes outliers into consideration.<br>

  **Capturing NaN with a new feature**:<br>
    **Assumption**: Data NOT missing completely at random.<br>
      Operation:<br>
      Replace the NaN in dataset with a new feature. ex: 0 and 1<br>
      Can also be replaced with a variable (for categorical variable). ex: “Missing”.<br>

  **Arbitrary Value Imputation**:<br>
    **Operation**:<br>
    Arbitrary value should not be the most frequent values.<br>
    Replace the NAN value with arbitrary value such as the extreme values in the dataset or any other values other than mean, median or mode.<br>

  **Frequent Category Imputation**:<br>
    **Assumption**: The amount of missing value is low.<br>
    **Operation**:<br>
    Find the number of missing values.<br>
    If there are few missing values: replace the missing values with most frequent value.<br>
  
* Remove outliers : 
  
Removing outliers from a dataset is an important step in data preprocessing to ensure that your data analysis and modeling are not unduly influenced by extreme or erroneous data points. Outliers are data points that deviate significantly from the rest of the data. There are various methods to identify and remove outliers, and the choice of method depends on the nature of your data and the specific goals of your analysis. Here's a general outline of the process:

1. Visual Inspection:
Start by visualizing your data using plots like histograms, box plots, scatter plots, or Q-Q plots. These can help you identify potential outliers.
Statistical Methods:

2. Use statistical methods to detect outliers. Some common techniques include:
Z-Score: Calculate the Z-Score for each data point, which measures how many standard deviations it is away from the mean. Data points with high absolute Z-Scores (typically greater than 3 or -3) can be considered outliers.
IQR (Interquartile Range): Calculate the IQR, which is the difference between the 75th percentile (Q3) and the 25th percentile (Q1). Data points outside the range [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR] are considered outliers.

3. Domain Knowledge:
Consider domain knowledge to identify outliers. Sometimes, data points that are outliers may have important information or may be valid data. In such cases, it's crucial to consult with domain experts before removing them.
Remove or Transform Outliers:

4. After identifying outliers, you can choose to:
Remove them: Delete the rows or data points that are identified as outliers. Be cautious when doing this, as it may lead to a loss of valuable information.
Transform them: Instead of removing outliers, you can transform them to be less extreme. Options include replacing them with the mean, median, or a predefined constant value, or applying data transformations like logarithms or winsorization.

5. Evaluate Impact:
Always assess how removing outliers affects your data distribution and analysis. It's essential to understand whether the removal significantly changes the results or insights drawn from the data.

6. Robust Algorithms:
When applicable, consider using robust statistical techniques or machine learning algorithms that are less sensitive to outliers, especially if you have reasons to believe that outliers are genuine data points.
Document and Justify:

7. Document the process of outlier detection and removal, including the criteria used and the rationale behind it. This documentation is essential for transparency and reproducibility of your analysis.
 
8. Iterate as Needed:
Depending on the impact of outlier removal, you may need to iterate through the process and re-evaluate your data.
Remember that the decision to remove outliers should be made thoughtfully, as it can have a significant impact on your analysis. It's important to strike a balance between data cleaning and retaining valuable information.
 
* Adjust for bias

  Adjusting for bias in data or in the context of data analysis is a critical step to ensure that your analysis and conclusions are as accurate and fair as possible. Bias can occur for various reasons, such as sampling methods, data collection processes, or algorithmic decisions. Here are some steps to help you adjust for bias in your data analysis:

1. Identify the Sources of Bias:
Before you can adjust for bias, you need to understand where bias may be present in your data or analysis. This could include bias in data collection, measurement error, sampling bias, or algorithmic bias.

2. Collect Comprehensive Data:
Ensure that your data collection process is as comprehensive as possible. Collecting data from a diverse and representative sample of the population or target group can help reduce bias due to underrepresentation.

3. Use Random Sampling:
If applicable, use random sampling techniques to select your data points. Random sampling helps ensure that each data point has an equal chance of being included, reducing selection bias.

4.Account for Missing Data:
Handle missing data appropriately. The way you handle missing data can introduce bias. Options include imputation methods or considering the missing data mechanism (missing completely at random, missing at random, or not missing at random) to make informed decisions about handling missing data.

5. Analyze Subgroups:
When analyzing data for bias, consider breaking down your analysis into subgroups based on relevant variables, such as age, gender, ethnicity, or other demographic factors. This can help identify bias affecting specific groups.

6.Evaluate Data Collection Procedures:
Examine the methods and procedures used to collect your data. Ensure that data collection tools and processes are designed to minimize bias. For example, consider using double-blind surveys to reduce response bias.

7.Use Fair and Unbiased Algorithms:
If you are using machine learning or algorithmic models, ensure that they are designed and trained to be fair and free from bias. Use techniques such as fairness-aware machine learning and algorithmic audits to detect and mitigate bias in models.

8. Sensitivity Analysis:
Perform sensitivity analysis to assess how changes in assumptions or methods affect your results. This can help you understand the impact of potential bias on your conclusions.

* Upsample
* Create synthetic data 

Feature selection<br>
Feature selection is an important aspect of building a machine learning model. Determining which features are important is essential for both performance and interpretability. Below are some methods and approaches to consider:
* Which features are important?
  * Statistical Tests: Correlation coefficients, chi-square tests, and t-tests can indicate the relationship between each feature and the target variable.
  *	Ensemble Methods: Algorithms like Random Forest and XGBoost provide feature importance metrics.
  *	Regularization Methods: Lasso and Elastic Net will shrink less important features towards zero, effectively performing feature selection.
  *	Domain Knowledge: Sometimes, the importance of features can be determined by domain experts.
  *	Wrapper Methods: Techniques like backward elimination and forward selection are model-based methods for feature selection.
    
* Partial dependencies/marginal contributions of each feature
  *	Partial Dependence Plots: These are used to visualize the effect of a single feature on the predicted outcome of a machine learning model.
  *	Individual Conditional Expectation (ICE) Plots: An extension of partial dependence plots, ICE plots visualize the dependence of the prediction on a feature for each instance.
  *	Shapley Values: These provide a measure of how each feature contributes to each individual prediction, allowing you to understand both global and local feature importance.
  
* Relations between the features
  * Correlation Matrix: A heat map of Pearson or Spearman correlation coefficients can show how features are related to each other.
  *	Multicollinearity Tests: The variance inflation factor (VIF) can be used to detect multicollinearity between features.
  *	Pair Plots: Scatter plot matrices can show pairwise relationships between numerical features.
  *	Cross-tabulation: For categorical features, cross-tabulation can help understand the relationship between different categories.
      
* Dependencies between the features
  *	Conditional Independence Tests: These tests can check if one variable is independent of another, given a third variable.
  *	Feature Interaction Terms: Adding interaction terms to the model can capture dependencies between features.
  *	Graphical Models: Bayesian networks or graphical models can represent conditional dependencies between features.
  *	Cluster Analysis: This can be used to find groups of highly similar features, indicating possible dependency.

* Considerations:
  *	Overfitting: Be cautious of overfitting when considering feature relations and dependencies. More features can make the model more complex and susceptible to overfitting.
  *	Interpreting Complexity: Complex relationships and dependencies between features can make the model less interpretable.
  *	Computation Cost: Some feature selection techniques and methods for assessing feature relations and dependencies can be computationally expensive.
It's often useful to employ a combination of these techniques to ensure a balanced approach to feature selection and understanding their interactions and dependencies.


Scale, normalize and transform
* When to scale?
    * Scaling means that we are tranforming the data so that it fits within a specific scale, like 0-1. This method is used when you're using methods based on measures of how far apart data points are.
    * It can help to balance the impact of all variables on the distance calculation and can help to imporve the performance of the algorithm.
* When to normalize?
    * The goal of normalization is to change the values of numerical columns in the dataset to use a common scale, without distorting differences in the ranges of values or losing information.
    * The data should be normalized when features have different ranges.
    * It also improves the performance and training stability of the model.
* When to transform?
    * Whenever a measurement variable does nit fit a normal distribution or has great different standard deviations in different groups it is better to perform a data tranformation.
    * Transforming variables can be done to correct outliers and assumption failures.

Graphical components:
    * Graphical components and diverse aspects are used in Data Visualisation to effectively represent and convey information.
These graphical components are the foundation of data visualization, and how they are used can have a big impact on the effectiveness of the visualizations.
The graphical components used are determined by the type of data, the message that is to be conveyed, and the sort of visualization that is being generated (for example, bar charts, scatter plots, line charts, and so on).

* X-position:
 The horizontal positioning of data points along a scale or axis is represented by an X-position. It usually refers to the dataset's independent variable or categories. The X-position is critical for organizing data along a similar scale, which allows readers to compare and analyze numbers within categories or across time
Example:
 * In a bar chart, the X-positions represent different categories or groups.
 * In a line chart, the X-axis usually represents time or continuous variables.
 
* Y - position  
* Color  
* Marks - Shape (Points, Bars,Lines, Areas, Volumes)  
* Channels (Position, Size, Angle/Slope, Color/Intensity/Hue,Texture)
* Animation    
* Faceting (small multiples) 


Chart types and fundamental graphs   
* Bar chart  (Categorical versus numeric)
   ----> A bar chart is a typical style of chart used in data science and data visualization to display categorical data (also known as qualitative or nominal data) in contrast to numeric data (quantitative data). Bar graphs are useful tools for showing and contrasting several categories or groups within a dataset visually.

  EXAMPLE OG BAR CHART:
![Categorical - Bar chart](https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/assets/114248445/ecb716fd-11c8-4289-8a05-ed24daca5d7b).
categorical data : Data that defines the categories or groups you want to compare is known as categorical data. Examples may be company names, locations, dates, or any other labels that lack numerals.
Numerical Information: This displays the numbers or measures related to each category. Any type of numerical data, including counts, frequencies, percentages, and continuous values, may be included.

* Scatter plot (Numeric versus numeric)
  ----> A  scatter plot is a sort of data visualization that is used to show the relationship or correlation between two sets of numeric data variables. Exploring patterns, trends, clusters, or outliers in the data is where it is most helpful. The x-axis and y-axis of a scatter plot both depict numerical variables.

  EXAMPLE OF SCATTERED GRAPH:

![SCATTERERD GRAPH](https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/assets/114248445/c6726dfe-2ed9-487b-a75f-66d4c4a8377d)

- The link between the two numerical variables is visually evaluated using scatter plots:
- A positive linear relationship exists between the variables if the data points form an approximately upward-sloping line, indicating that an increase in one variable tends to be associated with an increase in the other.
-  A negative linear relationship exists between the variables if the data points form an approximately downward-sloping line, indicating that an increase in one variable tends to be associated with a decrease in the other.
- No Linear Relationship: There may not be a linear relationship between the variables if there is no discernible pattern or if the points are dispersed at random.
    

* Line graphs (Sequence versus numeric) :

----> line graphs—also known as line charts or time series plots—are frequently used to show the link between a series of data points (such as time intervals or sorted categories) and an associated set of numerical values. The ability to display trends and patterns over time or among ordered categories makes these graphs especially helpful. 

EXAMPLE OF LINE GRAPH:

![line graph](https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/assets/114248445/94b3af77-5069-4b0a-9d99-7db3dd0f15cc)

Line graphs are used to visually assess trends, patterns, or changes in numeric values over the sequence:
-Increasing Trend: If the line generally moves upward from left to right, it indicates an increasing trend in the numeric values.
-Decreasing Trend: If the line generally moves downward from left to right, it indicates a decreasing trend.
-Steady or Flat Trend: If the line remains relatively constant, it indicates that the numeric values are not changing significantly over the sequence.
-Cyclical or Seasonal Patterns: In some cases, you may observe repeating patterns or cycles in the data.
Line graphs can also help identify outliers or sudden changes in the numeric values.

* Matrix (Rows versus columns)  :
----> Rows and columns make up a matrix, which is a structured data representation. Row and column indices serve as a means of identifying each member of a matrix. Matrices are a basic concept in linear algebra and other fields of data analysis and machine learning because they are used to organize, store, and modify data.

  EXAMPLE OF MATRIX :
  
![Matrix](https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/assets/114248445/37a55ccb-09ce-4f28-a826-50b203ecf354)

  
* Maps (Transformation)  

See the Data Visualisation Catalogue  <a href='https://datavizcatalogue.com'>https://datavizcatalogue.com</a>   



Legends, labels, annotations, and typeface  
* How to design and choose legends, labels, annotations and type   


Visual cognitive effectiveness   
* Quality of Data    
* Accuracy   
* Discriminability    
* Salience    
* Clutter  
* Grouping  


 
 
## Data Visualization Design

A collection of data visualization chart choosers, reference guides, cheat sheets, websites, books, tutorials and infographics about data visualization design.


*The Data Visualisation Catalogue* 

The Data Visualisation Catalogue <a href='https://datavizcatalogue.com'>https://datavizcatalogue.com</a>  

The Data Visualisation Catalogue is a project developed by <a href='http://www.severinoribecca.one'>Severino Ribecca</a> to create a library of different information visualisation types. The website serves as a learning and inspiration resource for those working with data visualisation. 


*The Chart Chooser Dissected*  

Identify the most effective graphical elements to use in your presentation from <a href='https://www.qlik.com/blog/third-pillar-of-mapping-data-to-visualizations-usage'>The Chart Chooser</a>. Decide what charts will provide the most convincing display of your quantitative evidence. 

Download a <a href='https://extremepresentation.typepad.com/files/choosing-a-good-chart-09.pdf'>pdf</a> of the chart chooser. 

*Financial Times Visual Vocabulary* 

A <a href='https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary'>PDF poster</a> (available in English, Japanese, traditional Chinese and simplified Chinese) to assist designers and journalists to select the optimal symbology for data visualisations, by the <a href='https://www.ft.com/visual-and-data-journalism'>Financial Times Visual Journalism Team</a>.  


*The Data Viz Project*  

The <a href='https://datavizproject.com'>Data Viz Project</a> is a website trying to present all relevant data visualizations, so you can find the right visualization and get inspired how to make them. It started out as an internal tool box at ferdio, an infographic and data visualization agency in Copenhagen, and grew into a public website where you and others can use it as a tool and inspiration.

*From Data to Viz*  

From <a href='https://www.data-to-viz.com/'>Data to Viz</a> is on online, interactive chart chooser that leads you to the most appropriate graph for your data. It also links to the code to build it (R, Python and D3) and lists common caveats you should avoid.

Also available as the poster shown. You can download the <a href='https://www.data-to-viz.com/#poster_full'>high-resolution image</a> or <a href='https://www.data-to-viz.com/poster.html'>Buy the Printed Poster.</a>



*The Data Visualization Checklist*  

This is a collaboration from Stephanie Evergreen & Ann K. Emery. The <a href='https://stephanieevergreen.com/wp-content/uploads/2020/12/EvergreenDataVizChecklist.pdf'>Data Visualization Checklist</a> is a compilation of 24 guidelines on how graphs should be formatted to best show the story in your data. The 24 guidelines are broken down into 5 sections: Text, Arrangement, Color, Lines, and Overall.

*Graph Selection Matrix*  

The <a href='https://www.perceptualedge.com/images/Effective_Chart_Design.pdf'>Graph Selection Matrix</a> comes from Stephen Few’s book, Show Me The Numbers, and is available as a stand-alone <a href='https://www.perceptualedge.com/images/Effective_Chart_Design.pdf'>PDF</a> download.

 
*Visualizing Percentages & Parts of a Whole*
 
Working with percentages is very common, and one of the most challenging parts of designing data visualizations. 


You can download a PDF of the reference sheet here: <a href='https://static1.squarespace.com/static/59df9853cd0f68dd29301c12/t/5c54cc23652dea724570e8c4/1549061155345/Visualizing-Percentages-20-Ways-InfoNewt.pdf'>Visualizing-Percentages-20-Ways-InfoNewt.pdf</a>     


*Graphic Cheat Sheet*  

The <a href='https://www.billiondollargraphics.com/GCS.pdf'>Graphic Cheat Sheet</a> was designed by Mike Parkinson, and is a very popular handout distributed at his conference talks. He has updated it numerous times over the years, and it’s available to download as a PDF. 60 different graphic types are grouped as Simple, Complex or Quantitative and shown when they can apply to be used to communicate 13 different types of data.


*The Chart Guide 4.0* 

Michiel Dullaert created the <a href='https://chart.guide/wp-content/uploads/2019/10/ChartGuide-402-web.pdf'>Chart Guide</a> for his data visualization classes, and has made it available to everyone through the website chart.guide as a downloadable <a href='https://chart.guide/wp-content/uploads/2019/10/ChartGuide-402-web.pdf'>PDF</a> or for purchase as a <a href='https://chart.guide/poster/'>printed poster</a>.


*Play Your Charts Right*  

Play Your Charts Rights is a free, downloadable <a href='https://www.geckoboard.com/uploads/play-your-charts-right.pdf'>PDF poster</a> with 12 great data visualization tips from Geckoboard. They will also send you a print poster upon request! Hang it in the office as a constant reminder for your team!

*How To Think Visually Using Visual Analogies*  

This <a href='https://blog.adioma.com/wp-content/uploads/2017/02/how-to-think-visually-using-visual-analogies-infographic.png'>infographic</a> from Anna Vital at Adioma groups 72 different visualization methods into four main categories: Charts & Diagrams, Abstract Analogies, Analogies, and Allegories. This goes beyond the traditional numerical data visualization methods to include more conceptual visual styles and diagrams often used in business environments.


*Qualitative Chart Chooser*   

Stephanie Evergreen and Jennifer Lyons collaborated to create the Qualitative Chart Chooser as a downloadable <a href='https://stephanieevergreen.com/wp-content/uploads/2021/07/Qualitative-Chooser.pdf'>PDF</a> to help researchers working with text, concept sand relationship data where traditional charts don’t apply. Version 2.0 includes two pages with a visual display of the chart types and decision matrix to help choose the appropriate display of information. There is also an updated Version 3.0 of the decision matrix.


<a href=''></a>

 
## Data Visualization articles and links 

The full content of the poster, along with links to related material, including research and examples of best practice. _This is a work in progress._

### General

* National Geographic: [Taking data visualisation from eye candy to efficiency](http://news.nationalgeographic.com/2015/09/150922-data-points-visualization-eye-candy-efficiency/)
* William S. Cleveland and Robert McGill: [Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods](http://info.slis.indiana.edu/~katy/S637-S11/cleveland84.pdf)
* Hadley Wickham: [A Layered Grammar of Graphics](http://vita.had.co.nz/papers/layered-grammar.pdf)
* Tracey L. Weissgerber et al: [Beyond Bar and Line Graphs: Time for a New Data Presentation Paradigm](http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002128)
* Numeroteca: [Uses and abuses of data visualisations in mass media](http://numeroteca.org/2016/05/18/uses-and-abuses-of-data-visualizations-in-mass-media/)
* Andy Cotgreave: [The inevitability of data visualization criticism](http://www.computerworld.com/article/3048315/data-analytics/the-inevitability-of-data-visualization-criticism.html)
* Alberto Cairo: ["Our reader" won't understand something as complicated as that!](http://www.thefunctionalart.com/2016/05/our-reader-wont-understand-something-as.html)
* Alberto Cairo: [Visualization's expanding vocabulary](http://www.thefunctionalart.com/2016/05/visualizations-expanding-vocabulary.html)

### Deviation

Emphasise variations (+/-) from a fixed reference point. Typically the reference point is zero but it can also be a target or a long-term average. Can also be used to show sentiment (positive/neutral/negative). *Example FT uses:* Trade surplus/deficit, climate change

#### Diverging bar

A simple standard bar chart that can handle both negative and positive magnitude values.

* Chart Doctor: [How the FT explained Brexit](https://www.ft.com/content/3bfc0aac-4ccd-11e6-88c5-db83e98a590a)

#### Diverging stacked bar

Perfect for presenting survey results which involve sentiment (eg disagree/neutral/agree).

#### Spine chart

Splits a single value into 2 contrasting components (eg Male/Female)

#### Surplus/deficit filled line

The shaded area of these charts allows a balance to be shown – either against a baseline or between two series.

### Correlation

Show the relationship between two or more variables. Be mindful that, unless you tell them otherwise, many readers will assume the relationships you show them to be causal (i.e. one causes the other). *Example FT uses:* Inflation & unemployment, income & life expectancy

* Chart Doctor: [The German election and the trouble with correlation](https://www.ft.com/content/94e3acec-a767-11e7-ab55-27219df83c97)

#### Scatterplot

The standard way to show the relationship between two continuous variables, each of which has its own axis.

* Chart Doctor: [The storytelling genius of unveiling truths through charts](https://www.ft.com/content/e2eba288-ef83-11e6-930f-061b01e23655)
* Maarten Lambrechts: [7 reasons you should use dot graphs](http://www.maartenlambrechts.com/2015/05/03/to-the-point-7-reasons-you-should-use-dot-graphs.html)
* Tim Brock: [Too Big Data: Coping with Overplotting](https://www.infragistics.com/community/blogs/tim_brock/archive/2015/04/21/too-big-data-coping-with-overplotting.aspx)
* Sara Kehaulani Goo: [The art and science of the scatterplot](http://www.pewresearch.org/fact-tank/2015/09/16/the-art-and-science-of-the-scatterplot/)
* Chart Doctor: [The storytelling genius of unveiling truths through charts](https://www.ft.com/content/e2eba288-ef83-11e6-930f-061b01e23655)
* *Examples:* [_FT_](https://www.ft.com/content/1ce1a720-ce94-3c32-a689-8d2356388a1f)

#### Line + Column

A good way of showing the relationship between an amount (columns) and a rate (line)

* Data Revelations: [Be Careful with Dual Axis Charts](http://www.datarevelations.com/be-careful-with-dual-axis-charts.html)
* DataHero: [The Do’s and Don’ts of Dual Axis Charts](https://datahero.com/blog/2015/04/23/the-dos-and-donts-of-dual-axis-charts/)
* Harvard Business Review: [Beware Spurious Correlations](https://hbr.org/2015/06/beware-spurious-correlations)

#### Connected scatterplot

Usually used to show how the relationship between two variables has changed over time.

* Robert Kosara: [The Connected Scatterplot for Presenting Paired Time Series](https://eagereyes.org/papers/the-connected-scatterplot-for-presenting-paired-time-series)
* Data Revelations: [Be Careful with Dual Axis Charts](http://www.datarevelations.com/be-careful-with-dual-axis-charts.html)
* *Examples:* [_Washington Post_](https://www.washingtonpost.com/apps/g/page/business/the-end-of-the-us-oil-boom-told-through-one-texas-companys-bust/1999/)

#### Bubble

Like a scatterplot, but adds additional detail by sizing the circles according to a third variable 

* Chart Doctor: [The storytelling genius of unveiling truths through charts](https://www.ft.com/content/e2eba288-ef83-11e6-930f-061b01e23655)
* *Examples:* [_FT_](https://ig.ft.com/managements-missing-women-data/)

#### XY heatmap

A good way of showing the patterns between 2 categories of data, less good at showing fine differences in amounts.

* Chart Doctor: [Use fewer maps to illustrate data better](https://www.ft.com/content/de3ef722-9514-11e6-a1dc-bdf38d484582)

### Ranking

Use where an item’s position in an ordered list is more important than its absolute or relative value. Don’t be afraid to highlight the points of interest. *Example FT uses:* Wealth, deprivation, league tables, constituency election results

#### Ordered bar

Standard bar charts display the ranks of values much more easily when sorted into order

#### Ordered column

See above.

#### Ordered proportional symbol

Use when there are big variations between values and/or seeing fine differences between data is not so important.

#### Dot strip plot

Dots placed in order on a strip are a space-efficient method of laying out ranks across multiple categories.

#### Slope

Perfect for showing how ranks have changed over time or vary between categories. 

#### Lollipop chart

Lollipops draw more attention to the data value than standard bar/column and can also show rank and value effectively.

### Distribution

Show values in a dataset and how often they occur. The shape (or ‘skew’) of a distribution can be a memorable way of highlighting the lack of uniformity or equality in the data. *Example FT uses:* Income distribution, population (age/sex) distribution

* Joey Cherdarchuk: [Visualising distributions](http://www.darkhorseanalytics.com/blog/visualizing-distributions-3)

#### Histogram

The standard way to show a statistical distribution - keep the gaps between columns small to highlight the ‘shape’ of the data

* Aran Lunzer and Amelia McNamara: [Exploring histograms](http://tinlizzie.org/histograms/)

#### Boxplot

Summarise multiple distributions by showing the median (centre) and range of the data

#### Violin plot

Similar to a box plot but more effective with complex distributions (data that cannot be summarised with simple average).

#### Population pyramid

A standard way for showing the age and sex breakdown of a population distribution; effectively, back to back histograms.

#### Dot strip plot

Good for showing individual values in a distribution, can be a problem when too many dots have the same value.

#### Dot plot

A simple way of showing the change or range (min/max) of data across multiple categories. 

#### Barcode plot

Like dot strip plots, good for displaying all the data in a table,they work best when highlighting individual values.

* Maarten Lambrechts: [Interactive strip plots for visualizing demographics](http://www.maartenlambrechts.com/2015/11/30/interactive-strip-plots-for-visualizing-demographics.html)

#### Cumulative curve

A good way of showing how unequal a distribution is: y axis is always cumulative frequency, x axis is always a measure.

### Change over Time

Give emphasis to changing trends. These can be short (intra-day) movements or extended series traversing decades or centuries. Choosing the correct time period is important to provide suitable context for the reader. *Example FT uses:* Share price movements, economic time series

* Flowing Data: [11 Ways to Visualize Changes Over Time – A Guide](http://flowingdata.com/2010/01/07/11-ways-to-visualize-changes-over-time-a-guide/)

#### Line 

The standard way to show a changing time series. If data are irregular, consider markers to represent data points 

* Chart Doctor: [A chart’s ability to mislead is off the scale](https://www.ft.com/content/3062d082-e3da-11e6-8405-9e5580d6e5fb)
* Office for National Statistics: [Does the axis have to start at zero? (Part 1 – line charts)](https://blog.ons.digital/2016/06/27/does-the-axis-have-to-start-at-zero-part-1-line-charts/)
* Quartz: [It's OK not to start your y-axis at zero](https://qz.com/418083/its-ok-not-to-start-your-y-axis-at-zero/)
* Vox: [Shut up about the y-axis. It should't always start at zero](https://www.youtube.com/watch?v=14VYnFhBKcY)
* Emily Schuch: [How to Make a Line Chart that Doesn't Lie](http://emschuch.github.io/Planned-Parenthood/)

#### Column 

Columns work well for showing change over time - but usually best with only one series of data at a time.

* Chart Doctor: [A chart’s ability to mislead is off the scale](https://www.ft.com/content/3062d082-e3da-11e6-8405-9e5580d6e5fb)
* Office for National Statistics: [Does the axis have to start at zero? (Part 2 – bar charts)](https://blog.ons.digital/2016/07/19/does-the-axis-have-to-start-at-zero-part-2-bar-charts/)


#### Line + column 

A good way of showing the relationship over time between an amount (columns) and a rate (line)

#### Stock price 

Usually focused on day-to-day activity, these charts show opening/closing and hi/low points of each day 

#### Slope 

Good for showing changing data as long as the data can be simplified into 2 or 3 points without missing a key part of story 

#### Area chart 

Use with care – these are good at showing changes to total, but seeing change in components can be very difficult 

#### Fan chart (projection) 

Use to show the uncertainty in future projections - usually this grows the further forward to projection 

#### Connected scatterplot 

A good way of showing changing data for two variables whenever there is a relatively clear pattern of progression. 

#### Calendar heatmap 

A great way of showing temporal patterns (daily, weekly, monthly) – at the expense of showing precision in quantity. 

#### Priestley timeline 

Great when date and duration are key elements of the story in the data.

* Chart Doctor: [Communicating with data: Timelines](https://www.ft.com/content/6f777c84-322b-11e6-ad39-3fee5ffe5b5b)
* *Examples:* [_FT_](https://www.ft.com/content/e7591532-9338-11e6-a1dc-bdf38d484582)

#### Circle timeline 

Good for showing discrete values of varying size across multiple categories (eg earthquakes by contintent). 

#### Seismogram 

Another alternative to the circle timeline for showing series where there are big variations in the data.

### Part-to-whole

Show how a single entity can bebroken down into its component elements. If the reader’s interest issolely in the size of the components,consider a magnitude-type chartinstead. *Example FT uses:* Fiscal budgets, company structures,national election results

* Flowing Data: [9 Ways to Visualize Proportions – A Guide](http://flowingdata.com/2009/11/25/9-ways-to-visualize-proportions-a-guide/)

#### Stacked column

A simple way of showing part-to-whole relationships but can be difficult to read with more than a few components.

* Robert Kosara: [Stacked bars are the worst](https://eagereyes.org/techniques/stacked-bars-are-the-worst)

#### Proportional stacked bar

A good way of showing the size and proportion of data at the same time – as long as the data are not too complicated. 

* Chart Doctor: [How to apply Marimekko to data](https://www.ft.com/content/3ee98782-9149-11e7-a9e6-11d2f0ebb7f0)

#### Pie

A common way of showing part-to-whole data – but be aware that it’s difficult to accurately compare the size of the segments.

* Robert Kosara: [Ye olde pie chart debate](https://eagereyes.org/blog/2015/ye-olde-pie-chart-debate)
* Robert Kosara: [Pie Charts – Unloved, Unstudied, and Misunderstood](https://eagereyes.org/talk/pie-charts-unloved-unstudied-and-misunderstood)
* Robert Kosara: [An Illustrated Tour of the Pie Chart Study Results](https://eagereyes.org/blog/2016/an-illustrated-tour-of-the-pie-chart-study-results)
* David Robinson: [How to replace a pie chart](http://varianceexplained.org/r/improving-pie-chart/)
* Office for National Statistics: [The humble pie chart: part 1](https://blog.ons.digital/2017/01/24/the-humble-pie-chart-part1/)
* Office for National Statistics: [The humble pie chart: part 2](https://blog.ons.digital/2017/02/23/the-humble-pie-chart-part2/)
* Ian Spence: [No humble pie: The origins and usage of a statistical chart](http://www.psych.utoronto.ca/users/spence/Spence%202005.pdf)
* Jeff Clark: [In defense of pie charts](http://www.neoformix.com/2007/InDefenseOfPieCharts.html)
* Stephen Few: [Save the Pies for Dessert](https://www.perceptualedge.com/articles/visual_business_intelligence/save_the_pies_for_dessert.pdf)


#### Donut

Similar to a pie chart – but the centre can be a good way of making space to include more information about the data (eg. total) 

#### Treemap

Use for hierarchical part-to-whole relationships; can be difficult to read when there are many small segments.

#### Voronoi

A way of turning points into areas – any point within each area is closer to the central point than any other centroid.

#### Arc

A hemicycle, often used for visualising political results in parliaments.

#### Gridplot

Good for showing % information, they work best when used on whole numbers and work well in multiple layout form.

#### Venn

Generally only used for schematic representation

#### Waterfall

Can be useful for showing part-to-whole relationships where some of the components are negative.

### Magnitude

Show size comparisons. These can berelative (just being able to seelarger/bigger) or absolute (need tosee fine differences). Usually theseshow a ‘counted’ number (for example, barrels, dollars or people) rather thana calculated rate or per cent. *Example FT uses:* Commodity production, marketcapitalisation

#### Column

The standard way to compare the size of things. Must always start at 0 on the axis

#### Bar

See above. Good when the data are not time series and labels have long category names.

#### Paired column

As per standard column but allows for multiple series. Can become tricky to read with more than 2 series.

#### Paired bar

See above.

#### Proportional stacked bar

A good way of showing the size and proportion of data at the same time – as long as the data are not too complicated.

* Chart Doctor: [How to apply Marimekko to data](https://www.ft.com/content/3ee98782-9149-11e7-a9e6-11d2f0ebb7f0)

#### Proportional symbol

Use when there are big variations between values and/or seeing fine differences between data is not so important.

#### Isotype (pictogram)

Excellent solution in some instances – use only with whole numbers (do not slice off an arm to represent a decimal).

#### Lollipop chart

Lollipop charts draw more attention to the data value than standard bar/column – does not HAVE to start at zero (but preferable).

#### Radar chart

A space-efficient way of showing value pf multiple variables– but make sure they are organised in a way that makes sense to reader.

#### Parallel coordinates

An alternative to radar charts – again, the arrngement of the variables is important. Usually benefits from highlighting values.

### Spatial

Used only when precise locations orgeographical patterns in data aremore important to the reader thananything else. *Example FT uses:* Locator maps, population density,natural resource locations, naturaldisaster risk/impact, catchment areas, variation in election results

* Chart Doctor: [Use fewer maps to illustrate data better](https://www.ft.com/content/de3ef722-9514-11e6-a1dc-bdf38d484582)
* Matthew Ericson: [When Maps Shouldn’t Be Maps](http://www.ericson.net/content/2011/10/when-maps-shouldnt-be-maps/)
* Mapbox: [7 data visualization techniques for location](https://blog.mapbox.com/7-data-visualizations-techniques-for-location-544c558cc960)

#### Basic choropleth (rate/ratio)

The standard approach for putting data on a map – should always be rates rather than totals and use a sensible base geography

* Vox: [The bad map we see every presidential election](http://www.vox.com/2016/5/17/11686328/bad-election-map)
* Vox: [This “bad” election map? It’s not so bad.](http://www.vox.com/2016/6/2/11828628/election-maps-hard)
* UX•Blog: [Telling the truth](http://uxblog.idvsolutions.com/2011/10/telling-truth.html)

#### Proportional symbol (count/magnitde)

Use for totals rather than rates – be wary that small differences in data will be hard to see.

* Stephen Few: [What Can’t Be Built with Bricks?](https://www.perceptualedge.com/blog/?p=1627)

#### Flow map

For showing unambiguous movement across a map.

#### Contour map

For showing areas of equal value on a map. Can use deviation colour schemes for showing +/- values

#### Equalised cartogram

Converting each unit on a map to a regular and equally-sized shape – good for representing voting regions with equal value.

* Chart Doctor: [How the FT explained Brexit](https://www.ft.com/content/3bfc0aac-4ccd-11e6-88c5-db83e98a590a)
* 5W Blog: [The power of cartograms and creating them easily](https://5wvelascoblog.com/2016/10/27/the-power-of-cartograms-and-creating-them-easily/)

#### Scaled cartogram (value)

Stretching and shrinking a map so that each area is sized according to a particular value.

* Chart Doctor: [The search for a better US election map](https://www.ft.com/content/3685bf9e-a4cc-11e6-8b69-02899e8bd9d1)
* 5W Blog: [The power of cartograms and creating them easily](https://5wvelascoblog.com/2016/10/27/the-power-of-cartograms-and-creating-them-easily/)
* Vox: [The bad map we see every presidential election](https://www.youtube.com/watch?v=hlQE4IGFc5A)

#### Dot density

Used to show the location of individual events/locations – make sure to annotate any patterns the reader should see.

* Chart Doctor: [The search for a better US election map](https://www.ft.com/content/3685bf9e-a4cc-11e6-8b69-02899e8bd9d1)

#### Heat map

Grid-based data values mapped with an intensity colour scale. As choropleth map – but not snapped to an admin/political unit.

* 5W Blog: [The power of cartograms and creating them easily](https://5wvelascoblog.com/2016/10/27/the-power-of-cartograms-and-creating-them-easily/)

### Flow

Show the reader volumes or intensity of movement between two or more states or conditions. These might belogical sequences or geographical locations. *Example FT uses:* Movement of funds, trade, migrants, lawsuits, information; relationship graphs.

* RJ Andrews: [Picturing the Great Migration](https://medium.com/info-we-trust/picturing-the-great-migration-9e4b5a3eca8a)

#### Sankey (aka river plot)

Shows changes in flows from one condition to at least one other; good for tracing the eventual outcome of a complex process. 

* Chart Doctor: [Data visualisation: it is not all about technology](https://www.ft.com/content/aba6c58e-5a8e-11e7-9bc8-8055f264aa8b)

#### Waterfall

Designed to show the sequencing of data through a flow process, typically budgets. Can include +/- components.

#### Chord

A complex but powerful diagram which can illustrate 2-way flows (and net winner) in a matrix.

#### Network

Used for showing the strength and inter-connectedness of relationships of varying types. 

- - - 

Todo:

### Uncertainty

* Scientific American: [Visualising uncertain weather](https://blogs.scientificamerican.com/sa-visual/visualizing-uncertain-weather/)
* Oli Hawkins: [Animating uncertainty](http://olihawkins.com/2013/09/2)

### Animation

* Chart Doctor: [The storytelling genius of unveiling truths through charts](https://www.ft.com/content/e2eba288-ef83-11e6-930f-061b01e23655)
* Evan Sinar: [Use Animation to Supercharge Data Visualization](https://medium.com/@EvanSinar/use-animation-to-supercharge-data-visualization-cd905a882ad4)

### Interactivity

* Chart Doctor: [Why the FT creates so few clickable graphics](https://www.ft.com/content/c62b21c6-7feb-11e6-8e50-8ec15fb462f4)
* Gregor Aisch: [In defense of interactive graphics](https://www.vis4.net/blog/posts/in-defense-of-interactive-graphics/)
* Zan Armstrong: [Why choose? Scrollytelling and steppers](https://medium.com/@zanarmstrong/why-choose-scrollytelling-steppers-155a59dd97fe))

### Map projections

### Colour


 
