# Quiz Questions: Federated Learning - Privacy and Utility in HAR

## Question 1: Federated Learning Basics

What is the main advantage of federated learning compared to traditional centralized machine learning?

A) It trains models faster than centralized approaches  
B) It always achieves higher accuracy than centralized methods  
C) It keeps raw data on local devices instead of sending it to a central server  
D) It requires less computational power  
E) It works only with image data  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** The fundamental benefit of federated learning is privacy preservation - raw data never leaves the client devices (smartphones, IoT devices, etc.). Only model updates are sent to the server, protecting sensitive user information.

**Why others are incorrect:**
- A: Federated learning is typically slower due to communication overhead across multiple rounds
- B: Federated learning usually achieves slightly lower accuracy (1-5%) due to non-IID data and privacy constraints
- D: It actually requires more total computation distributed across clients
- E: Federated learning works with any data type - text, sensor data, tabular data, images, etc.

---

## Question 2: Privacy in Federated Learning

In the chapter's HAR example with 30 smartphone users, what information do clients send to the central server during federated learning?

A) Raw sensor readings from accelerometer and gyroscope  
B) Personal user information and activity labels  
C) Only the neural network model weights/parameters  
D) GPS location and movement patterns  
E) Complete activity recognition history  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** Clients only send trained model parameters (weights) to the server after local training. This is approximately 300 KB of numerical values representing the neural network, not the actual sensor data.

**Why others are incorrect:**
- A: Raw sensor data stays on the device - this is the whole point of federated learning
- B: User information is never transmitted to preserve privacy
- D: Location data is not shared in federated learning
- E: Activity history remains private on the user's device

---

## Question 3: FedAvg Algorithm

In the Federated Averaging (FedAvg) algorithm, how does the server combine model updates from multiple clients?

A) It picks the best performing client's model and discards others  
B) It takes a simple average of all client models equally  
C) It takes a weighted average based on each client's dataset size  
D) It randomly selects one client model per round  
E) It only uses models from clients with the highest accuracy  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** FedAvg uses weighted averaging where clients with more data samples have proportionally more influence. For example, a client with 400 samples contributes more to the global model than a client with 40 samples (10× weight difference).

**Why others are incorrect:**
- A: All participating client updates are used, not just the best one
- B: Simple averaging would give equal weight to clients with 40 samples and 400 samples, which is unfair
- D: Random selection would waste the training effort of other clients
- E: All selected clients contribute regardless of individual accuracy

---

## Question 4: Communication Rounds

The chapter mentions training federated learning for 10 communication rounds with 5 out of 30 clients participating per round. How many total client updates does the server receive?

A) 10 updates  
B) 30 updates  
C) 50 updates  
D) 150 updates  
E) 300 updates  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** Simple calculation: 10 rounds × 5 clients per round = 50 total client updates received by the server.

**Why others are incorrect:**
- A: This would be if only 1 client participated per round
- B: This is the total number of clients, not updates
- D: This would be if all 30 clients participated in each of the 5 rounds (incorrect interpretation)
- E: This would be if all 30 clients participated in all 10 rounds

---

## Question 5: Non-IID Data

What does "non-IID" data mean in federated learning?

A) Data that is identical across all clients  
B) Data that each client has different statistical properties and distributions  
C) Data that is always sorted in alphabetical order  
D) Data that has been normalized and standardized  
E) Data that contains only numerical values  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** Non-IID stands for "non-Independent and Identically Distributed." In the HAR example, different users have different activity patterns - one person might walk more, another might sit more. Client sample sizes also vary (40 to 408 samples).

**Why others are incorrect:**
- A: This describes IID data, the opposite of what federated learning typically deals with
- C: IID has nothing to do with data sorting
- D: Normalization is a preprocessing step, unrelated to IID vs non-IID
- E: Non-IID refers to statistical distribution, not data types

---

## Question 6: Differential Privacy Basics

What is the purpose of adding noise to model updates in Differential Privacy (DP-FedAvg)?

A) To make the model train faster  
B) To prevent anyone from determining if a specific person's data was used in training  
C) To improve the accuracy of the model  
D) To reduce the size of data transmitted  
E) To make the code run more efficiently  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** Differential privacy adds calibrated random noise to ensure that an observer cannot reliably determine whether any individual's data was included in the training set, providing mathematical privacy guarantees.

**Why others are incorrect:**
- A: Adding noise typically slows convergence, not speeds it up
- C: Noise decreases accuracy (privacy-utility tradeoff) - the chapter shows 3-12% accuracy drops
- D: Noise doesn't change transmission size; the same model parameters are sent
- E: Adding noise adds computational overhead, not efficiency

---

## Question 7: Privacy Budget (Epsilon)

According to the chapter's results, what happens to model accuracy as the privacy budget ε (epsilon) decreases from 10.0 to 0.1?

A) Accuracy increases because privacy improves the model  
B) Accuracy stays the same regardless of epsilon value  
C) Accuracy decreases - stronger privacy (lower ε) means lower accuracy  
D) Accuracy first increases then decreases  
E) The model stops working completely  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** This demonstrates the privacy-utility tradeoff. Lower ε means stronger privacy but requires more noise, reducing accuracy:
- ε=10.0: 95.84% accuracy (weak privacy)
- ε=1.0: 92.73% accuracy (GDPR-compliant)
- ε=0.1: 84.07% accuracy (maximum privacy)

**Why others are incorrect:**
- A: Privacy mechanisms always trade some accuracy for privacy protection
- B: Epsilon directly controls noise magnitude, which affects accuracy
- D: The relationship is monotonic - more privacy consistently means less accuracy
- E: The model still works at ε=0.1, just with reduced accuracy

---

## Question 8: Dataset Information

How many activity classes does the UCI HAR dataset classify in the chapter's extended version?

A) 2 classes  
B) 6 classes (basic activities only)  
C) 12 classes (basic activities + postural transitions)  
D) 30 classes (one per client)  
E) 561 classes (one per feature)  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** The chapter uses the extended UCI HAR dataset with 12 activity classes:
- 6 basic activities: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING
- 6 postural transitions: STAND_TO_SIT, SIT_TO_STAND, SIT_TO_LIE, LIE_TO_SIT, STAND_TO_LIE, LIE_TO_STAND

**Why others are incorrect:**
- A: This would be binary classification, not the multi-class HAR problem
- B: This is only the basic activities, missing the transitions
- D: 30 is the number of clients (users), not activity classes
- E: 561 is the number of input features, not output classes

---

## Question 9: Communication Efficiency

Why does federated learning use less communication bandwidth compared to sending raw sensor data for centralized training (over multiple training iterations)?

A) Model parameters are compressed to 1 KB  
B) Model updates (300 KB) are smaller than repeatedly sending raw data for multiple epochs  
C) Federated learning doesn't use any network communication  
D) The server doesn't need to receive any information from clients  
E) Only one client sends data in federated learning  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** For 10 training epochs centrally, the server must load all client data repeatedly (198 MB total internal movement). Federated learning sends model parameters (~300 KB per client update) over 10 rounds = 30 MB total, achieving 6.6× efficiency.

**Why others are incorrect:**
- A: Model parameters are ~300 KB, not 1 KB
- C: Federated learning requires communication for model distribution and update aggregation
- D: Clients must send model updates to the server
- E: Multiple clients (5 per round) participate and send updates

---

## Question 10: Accuracy Results

What accuracy did Standard FedAvg (without differential privacy) achieve on the HAR test set compared to the centralized baseline?

A) 97.73% (same as centralized)  
B) 96.22% (1.51% lower than centralized)  
C) 92.73% (5% lower than centralized)  
D) 84.07% (much lower than centralized)  
E) 99.5% (higher than centralized)  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** Standard FedAvg achieved 96.22% compared to 97.73% centralized baseline, representing a 1.51% accuracy cost for model-level privacy (keeping data on devices).

**Why others are incorrect:**
- A: Federated learning typically has slight accuracy degradation due to non-IID data
- C: This is the accuracy with ε=1.0 differential privacy, not standard FedAvg
- D: This is the accuracy with strong ε=0.1 differential privacy
- E: Federated learning rarely exceeds centralized performance on the same data

---

## Question 11: Local Training

In the FedAvg algorithm, what happens during the "local training" phase on each client device?

A) The client sends its raw data to the server  
B) The client downloads the global model and trains it on its local private data  
C) The client deletes its local data  
D) The client waits for other clients to finish  
E) The client evaluates other clients' models  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** Each selected client downloads the current global model from the server, then performs local training using its own private dataset for E epochs (2 epochs in the chapter's setup), and finally sends the updated model weights back to the server.

**Why others are incorrect:**
- A: Raw data never leaves the client device in federated learning
- C: Clients keep their data for future training rounds
- D: Clients train in parallel, not sequentially waiting for others
- E: Clients only train their own local model, not evaluate others

---

## Question 12: Privacy Regulations

Which privacy regulations does the chapter mention as motivation for using federated learning?

A) COPPA and FERPA  
B) GDPR and HIPAA  
C) SOX and PCI-DSS  
D) DMCA and CAN-SPAM  
E) CCPA and GLBA  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** The chapter specifically mentions:
- GDPR (General Data Protection Regulation) - European Union data privacy law, Article 5 and Article 25
- HIPAA (Health Insurance Portability and Accountability Act) - U.S. healthcare data privacy law

**Why others are incorrect:**
- A: COPPA (children's online privacy) and FERPA (education records) are not mentioned
- C: SOX (financial reporting) and PCI-DSS (payment card security) are not the focus
- D: DMCA (copyright) and CAN-SPAM (email marketing) are unrelated to this context
- E: CCPA (California privacy) and GLBA (financial privacy) are not discussed in the chapter

---

## Question 13: Cross-Domain Validation

The chapter validates federated learning on a second dataset (German Credit). Why did this dataset show a higher privacy cost (4.39%) compared to HAR (1.51%)?

A) The credit dataset had more clients  
B) The credit dataset was larger  
C) The credit dataset was smaller with only 1,000 samples vs. 10,299 samples in HAR  
D) The credit dataset had more features  
E) The credit dataset used a different programming language  

**Correct Answer: C**

**Explanation:**  
**Why C is correct:** Smaller datasets amplify the impact of client heterogeneity and non-IID effects. With 10× fewer samples, the credit dataset (1,000 samples, 8 clients) experiences greater accuracy degradation than HAR (10,299 samples, 30 clients).

**Why others are incorrect:**
- A: Credit had fewer clients (8 vs. 30), which actually makes the problem harder
- B: Credit dataset is smaller, not larger
- D: Credit has fewer features (24 vs. 561), so this isn't the cause
- E: Programming language doesn't affect privacy-accuracy tradeoffs

---

## Question 14: Gradient Clipping

In Differential Privacy, why is gradient clipping applied before adding noise?

A) To make the code run faster  
B) To limit how much any single training sample can influence the model update  
C) To increase the model's accuracy  
D) To compress the data for transmission  
E) To encrypt the gradients  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** Gradient clipping bounds individual gradient norms (e.g., to C=1.0), ensuring no single training example dominates the update. This controls the "sensitivity" of the function, which determines how much noise is needed for privacy.

**Why others are incorrect:**
- A: Clipping adds computational overhead, not speed
- C: Clipping and noise typically reduce accuracy for privacy gain
- D: Clipping affects gradient magnitude, not data compression
- E: Clipping is not an encryption method; it's a privacy mechanism

---

## Question 15: Practical Deployment

For a consumer fitness tracker app (like Fitbit), which privacy budget (ε) does the chapter recommend as a good balance between privacy and accuracy?

A) ε = 0.1 (maximum privacy, research only)  
B) ε = 1.0 (GDPR-compliant, acceptable accuracy ~92-95%)  
C) ε = 10.0 (weak privacy, near-centralized accuracy)  
D) ε = 100.0 (no privacy protection)  
E) No differential privacy needed  

**Correct Answer: B**

**Explanation:**  
**Why B is correct:** The chapter's practical deployment guidelines recommend ε = 1.0 for consumer IoT applications like fitness trackers. This provides GDPR compliance while maintaining 92-95% accuracy, which users find acceptable for activity tracking.

**Why others are incorrect:**
- A: ε = 0.1 gives only 84% accuracy - too low for good user experience in consumer apps
- C: ε = 10.0 provides weak privacy protection, not suitable for regulatory compliance
- D: Very large epsilon provides essentially no privacy guarantee
- E: Differential privacy is recommended for proper privacy protection, especially under GDPR

---
