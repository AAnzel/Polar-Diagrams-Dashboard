# User Study Concept --- Enhanced Polar Diagrams
### Author: Aleksandar Anžel

[1] `Tory, M. (2014). User Studies in Visualization: A Reflection on Methods. In: Huang, W. (eds) Handbook of Human Centric Visualization. Springer, New York, NY. https://doi.org/10.1007/978-1-4614-7485-2_16`

## The Purpose

Using [1] we classify our user study as an "Evaluation", and more specifically a type of evaluation where we want to "Evaluate one visualization technique, tool, or interaction technique". We chose this because "the competing approaches are so primitive that comparison against them would be pointles"[1]. The previous work does not provide functionalities that enable users to achieve complex tasks.

We plan to utilize a users study known as "Usability study" and collect data via a Questionnaire.

In essence, we evaluate the enhanced version of polar-diagrams library that implements overview+detail, small multiple, aggregation, filtering, and Cartesian linking. We want to see if the tool is easy to use and understandable to both novice and expert users.

## Research Aims

We aim to answer the following questions and address multiple context details within:

- Does the new enhanced version of the Scaled Mutual Information diagram that implements overview+diagram, aggregation, filtering, and Cartesian linking enable users to easily solve tasks that the Scaled MI diagram is designed for?
    1. The improved diagrams should be domain-agnostic and target both novice and expert users.
    2. The users should be able to solve tasks such as:
        - Similarity analysis
        - Outlier detection
        - Pattern (cluster) detection
        - Model ranking
        - Model assessment over multiple statistical measures
    3. The tasks are deemed successful if the users are able to use filtering (implemented with multi-selection and brushing) and Cartesian linking to:
        1. Easily detect which model is most similar to the reference model
        2. Detect outliers
        3. Detect clusters
        4. Easily rank the models using VI
        5. Easily compare the models using other measures such as Entropy and Scaled MI


## Research Methods and Experimental Designs

The data for the study is collected using an online questionnaire. The questions are designed to thoroughly evaluate the proposed enhanced version. The users are supposed to answer multiple-choice questions for each task. Time to completion is measured while solving each task.

We used the following tool to interview participants: `Leiner, D. J. (2021). SoSci Survey (Version 3.2.31) [Computer software]. Available at https://www.soscisurvey.de`. The following data set was used with the polar-diagrams library for evaluation: `Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems (Vol. 47, Issue 4, pp. 547–553). Elsevier BV. https://doi.org/10.1016/j.dss.2009.05.016`.

The process loops through three sections: Tutorial, Training, and Test. The Tutorial section provides users with a basic understanding of the functionality that will be examined in the following Training and Test tasks. The Training task is simple, and the user is presented with feedback upon answering it. The Test task is more complex and does not provide any feedback. The answers are randomly shuffled for each user. The train-test pairs were as follows:
1. First pair (covers understanding the Taylor diagram and the similarity principle)
    1. Train 1: Which model is closest to the reference model?
        1. Wine_2
        2. Wine_7
        3. Wine_0
        4. Wine_15 (correct)
        5. Wine_3
        6. Wine_18
    2. Test 1: Which 3 models are the furthest from the reference model?
        1. Wine_19, Wine_6, and Wine_7
        2. Wine_15, Wine_11, and Wine_3
        3. Wine_18, Wine_13, and Wine_2
        4. Wine_17, Wine_9, and Wine_7
        5. Wine_18, Wine_17, and Wine_9 (correct)
        6. Wine_0, Wine_5, and Wine_4
2. Second pair (covers the Overview and the Legend)
    1. Train 2: How many clusters are there, not counting the reference model?
        1. 0
        2. 5
        3. 2
        4. 7
        5. 6 (correct)
        6. 3
    2. Test 2: How many models are in Cluster 4?
        1. 3
        2. 2
        3. 7 (correct)
        4. 5
        5. 1
        6. 6
3. Third pair (covers filtering with legend multi-select or overview brushing)
    1. Train 3: Select Cluster 1 using the legend or overview.  Which individual model at the center of that cluster has the middle/median variation of information (VI)?
        1. Wine_5 (correct)
        2. Wine_10
        3. Wine_4
        4. Wine_0
        5. Wine_14
        6. Wine_6
    2. Test 3: What model from Cluster 1 is furthest from Cluster 5?
        1. Wine_4
        2. Wine_10
        3. Wine_7
        4. Wine_5
        5. Wine_9
        6. Wine_0 (correct)
4. Fourth pair (covers tooltip and Cartesian linking)
    1. Train 4: Select models Wine_4 and Wine_17. Check the tooltip and Cartesian-linking plot. What is the approximate sum of their entropies?
        1. Approximately  8
        2. Approximately  4
        3. Approximately  10 (correct)
        4. Approximately  1
        5. Approximately  15
        6. Approximately  12
    2. Test 4: Select Cluster 3 and Cluster 5. What are the ranges of variation of information (VI) within these two clusters? Provide the minimum and maximum VI values for these clusters, starting from smallest to largest.
        1. 3.0 - 4.5  and  3.6 - 4.0
        2. 2.3 - 2.9  and  4.8 - 5.7
        3. 1.2 - 1.6  and  3.6 - 4.0
        4. 2.5 - 3.2  and  4.2 - 5.2
        5. 1.2 - 1.6  and  4.8 - 5.7 (correct)
        6. 0.5 - 2.2  and  3.6 - 4.0

## Ethical Considerations

The questionnaire collects only study-related and sociodemographics data, hence ensuring maximum privacy protection of the participants.

Study-related data is in the form of questions listed in the previous section. Besides this, we also ask participants study-relevant questions. At the end, users are also asked to evaluate the dashboard using System Usability Scale (`Brooke, John (1996). "SUS: a "quick and dirty" usability scale". In P. W. Jordan; B. Thomas; B. A. Weerdmeester; A. L. McClelland (eds.). Usability Evaluation in Industry. London: Taylor and Francis.`)

Sociodemographics data is consisted of the following features:
1. Gender (multiple options)
2. Age group (each age group is given in ten years increments, starting with 20-30 and ending with 70-80)
3. Highest Degree (multiple options)
4. Field of experience (multiple options, multiple selections)
5. Years of experience (each age group is given in five years increments, starting with <5 and ending with >35)
6. Subjective graph literacy test (`Garcia-Retamero R, Cokely ET, Ghazal S, Joeris A. Measuring Graph Literacy without a Test: A Brief Subjective Assessment. Medical Decision Making. 2016;36(7):854-867. doi:10.1177/0272989X16655334`)
4. Experience with charts in polar coordinate system (yes or no)
5. Experience with the summary polar diagrams such as the Taylor and Mutual Information diagrams (yes or no)


---

## Perplexity's output on how to do user study when evaluating only one tool

To evaluate your visualization tool using a usability study without comparing it to other tools, you should focus on assessing its effectiveness, efficiency, and user satisfaction. Here's how you can approach this and formulate your research questions:

1. Define your evaluation goals: First, determine what aspects of your tool you want to evaluate. This could include ease of use, learnability, user satisfaction, and the effectiveness of specific visualization techniques implemented in your tool.
2. Formulate research questions: Your research questions should be specific to your tool and its intended purpose. Some examples include:

    1. How effectively does the tool allow users to complete specific visualization tasks?
    2. To what extent do users find the interface intuitive and easy to navigate?
    3. How well do users understand and interpret the visualizations produced by the tool?
    4. What is the learning curve for new users to become proficient with the tool?
    5. How satisfied are users with the overall functionality and performance of the tool?

3. Design the usability study: Create a study that addresses your research questions. This may involve:

    1. Task-based evaluations: Ask participants to complete specific tasks using your tool and observe their performance
    2. Think-aloud protocols: Have users verbalize their thoughts as they interact with the tool
    3. Questionnaires and surveys: Gather quantitative and qualitative feedback on user experience and satisfaction
    4. Heuristic evaluation: Assess the tool against established usability principles

4. Collect and analyze data: Gather both quantitative (e.g., task completion times, error rates) and qualitative (e.g., user feedback, observations) data. Analyze this data to answer your research questions and identify areas for improvement
5. Evaluate specific visualization techniques: Since your tool implements multiple visualization techniques, you may want to assess the effectiveness of each technique for different types of data or tasks. This can help you determine which techniques are most useful and where improvements might be needed
6. Consider user experience factors: Evaluate aspects such as interface clarity, data interactivity, and overall accessibility of your tool
7. Iterate and improve: Use the insights gained from your usability study to refine and enhance your tool. Consider conducting follow-up studies to assess the impact of any changes made

By following this approach, you can conduct a comprehensive usability evaluation of your visualization tool without the need for direct comparisons to other tools. This will provide valuable insights into its strengths, weaknesses, and areas for potential improvement.



### Evaluating Specific Visualization Techniques

To evaluate specific visualization techniques in your tool, focus on assessing their effectiveness, usability, and user comprehension. Here's how you can address this:

1. **Identify the specific techniques**: Clearly define which visualization techniques your tool implements and which ones you want to evaluate.

2. **Design task-based evaluations**: Create specific tasks that users need to complete using each visualization technique. These tasks should be representative of real-world scenarios where the technique would be applied.

3. **Establish evaluation criteria**: Develop a set of criteria to assess each technique. This may include:

   - Clarity: How easy is it for users to understand the information presented?
   - Accuracy: Does the visualization accurately represent the underlying data?
   - Interpretability: Can users correctly interpret the information from the visualization?
   - Efficiency: How quickly can users extract relevant information?
   - User satisfaction: How do users feel about using this particular technique?

4. **Collect quantitative and qualitative data**:
   - Quantitative: Measure task completion times, error rates, and accuracy of interpretations.
   - Qualitative: Gather user feedback through think-aloud protocols, interviews, or surveys.

5. **Compare techniques**: If your tool implements multiple visualization techniques, you can compare their effectiveness for different types of data or tasks. This can help identify which techniques are most suitable for specific scenarios.

6. **Consider perceptual aspects**: Evaluate how well each technique aligns with principles of human visual perception. For example, assess if the technique uses color, size, or position effectively to convey information.

7. **Assess scalability**: Determine how well each technique handles different volumes of data. Some visualizations may work well for small datasets but become cluttered or unreadable with larger ones.

8. **Evaluate learning curve**: Assess how easily users can understand and effectively use each visualization technique. This is particularly important for more complex or novel techniques.

9. **Check for potential biases**: Ensure that the visualizations don't inadvertently introduce biases or misrepresentations of the data.

10. **Conduct expert reviews**: In addition to user testing, consider having visualization experts evaluate the techniques based on established principles and best practices.

By systematically evaluating each visualization technique using these methods, you can gain valuable insights into their strengths, weaknesses, and overall effectiveness. This approach will help you identify which techniques are most successful in your tool and where improvements might be needed. Remember to document your evaluation process and findings thoroughly, as this will be crucial for reporting your results and making informed decisions about future developments of your tool.

### Quantifying Evaluation Criteria for Visualization Tools

To quantify evaluation criteria for your visualization tool, focus on developing measurable metrics that align with your research questions. Here's how you can approach this:

#### 1. Define specific metrics for each criterion

For each evaluation criterion, establish clear, quantifiable metrics. For example:

- **Effectiveness**: Measure task completion rates and accuracy of data interpretation.
- **Efficiency**: Record task completion times and the number of steps required to perform specific actions.
- **User satisfaction**: Use standardized questionnaires with numerical scales (e.g., 1-5 Likert scale) to assess user experience.

#### 2. Utilize performance metrics

Collect quantitative data on tool performance, such as:

- **Response time**: Measure the speed at which visualizations are generated or updated.
- **Data processing capability**: Assess the tool's ability to handle different volumes of data.
- **Accuracy of statistical calculations**: Compare the tool's results with known correct values.

#### 3. Implement usability heuristics

Use established usability heuristics and convert them into quantifiable measures. For instance:

- **Interface clarity**: Count the number of user errors or misclicks during specific tasks.
- **Learnability**: Measure the time taken for users to successfully complete tasks without assistance.
- **Consistency**: Assess the number of interface elements that follow established conventions.

#### 4. Assess visualization-specific criteria

Evaluate the effectiveness of your visualization techniques using metrics such as:

- **Data-ink ratio**: Calculate the proportion of ink used for displaying data versus non-data elements.
- **Chart junk**: Quantify unnecessary visual elements that don't contribute to data understanding.
- **Color effectiveness**: Measure the accuracy and speed of color-based data identification tasks.

#### 5. Utilize eye-tracking data

If available, use eye-tracking technology to gather quantitative data on:

- **Fixation duration**: Measure how long users focus on specific elements of the visualization.
- **Scan paths**: Analyze the efficiency of users' visual search patterns.

#### 6. Implement error analysis

Quantify errors in data interpretation or task completion:

- **Error rate**: Calculate the percentage of tasks completed incorrectly.
- **Error severity**: Develop a scale to rate the impact of different types of errors.

#### 7. Use comparative metrics

If comparing multiple visualization techniques within your tool:

- **Preference ratings**: Ask users to rank techniques on a numerical scale.
- **Performance differences**: Calculate the percentage improvement in task completion time or accuracy between techniques.

#### 8. Assess data access and integration

Quantify the tool's data handling capabilities:

- Number of supported data formats and sources.
- Time required to integrate data from multiple sources.

#### 9. Evaluate output and content management

Measure the effectiveness of sharing and exporting visualizations:

- Number of supported export formats.
- Time required to generate reports or share visualizations.

By quantifying these evaluation criteria, you'll be able to conduct a more objective assessment of your visualization tool. This approach allows for statistical analysis of your results, providing stronger evidence for the tool's effectiveness and areas for improvement. Remember to choose metrics that are most relevant to your specific research questions and the intended use of your visualization tool.