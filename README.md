# Cognitive Robotics
This repository contains a final project in **Cognitive Robotics & Artificial Vision** focused on building an integrated **ROS-based system** for the **Pepper robot**. The system combines computer vision, speech processing, dialogue management, and robot control to enable natural human-robot interaction in real-world environments such as a bar, market, boutique, or game store.

## Project Overview

The goal of the project is to allow Pepper to:

- recognize and track people in real time
- classify pedestrian attributes such as **gender**, **bag**, and **hat**
- manage spoken interactions through **speech-to-text**, **Rasa**, and **text-to-speech**
- answer user requests about detected people and competition-related information
- interact in a more natural and engaging way through gestures, head tracking, and animations

The project was developed at the **University of Salerno** for the course **Cognitive Robotics & Artificial Vision**, Academic Year **2024–2025**.

## Architecture

The system is implemented on **Ubuntu 20.04** using **ROS** and **Rasa**, following a modular architecture based on:

- **Publish/Subscribe** communication for perception and interaction flows
- **ROS services** for synchronous request-response behaviors
- **NAOqi APIs** for Pepper-specific capabilities such as motion, posture, speech, awareness, and animation

The report describes the architecture as a ROS-based system integrating audio nodes, Rasa nodes, engagement nodes, and Pepper nodes.

## Main Modules

### 1. Audio Module
Responsible for capturing and processing user speech.

Components include:
- **voice_detection**: activates or pauses listening depending on whether Pepper is speaking and whether a person is detected
- **asr**: converts microphone audio into text using **Google Speech Recognition**

This synchronization prevents Pepper from listening to itself while speaking.

### 2. Dialogue Management Module
Built with **Rasa** to manage natural language understanding and dialogue flow.

It includes:
- intents
- entities
- rules
- stories
- forms
- custom actions

The chatbot can manage requests such as:
- searching for a person with given attributes
- counting people with certain characteristics
- retrieving IDs and trajectory information
- answering group ranking and score questions

The project relies heavily on hand-crafted NLU examples and a rule-based dialogue structure for flexibility and control.

### 3. Engagement Module
Responsible for detecting people and managing Pepper’s interaction behavior.

Main nodes:
- **detector_node**: detects people/faces from camera frames using **EfficientDet D1 COCO17 TPU-32**
- **person_engagement**: tracks user presence and triggers appropriate robot behavior

This enables Pepper to engage with users, wait for interaction, and reset its head when a person is no longer visible.

### 4. Pepper Control Module
Handles Pepper-specific capabilities through ROS nodes and NAOqi services.

Included functionalities:
- **face tracking**
- **head motion control**
- **wake-up / rest state management**
- **text-to-speech**
- **animated speech**
- **gesture / animation triggering**

These modules improve the naturalness of the interaction by combining speech, motion, and tracking.

## Video Analytics

The vision system is based on **EfficientDet D1 COCO17 TPU-32**, chosen for its balance between speed and accuracy. It supports reliable human detection even when users are far away, partially in profile, or moving. This makes the engagement process more stable and robust in dynamic real-world scenarios.

## Speech-to-Text

The speech recognition module uses **Google Speech Recognition**. According to the report, this choice was motivated by:
- increased efficiency
- improved accessibility
- enhanced user experience
- cost savings
- improved accuracy

## Rasa Configuration

The NLU pipeline includes components such as:

- `WhitespaceTokenizer`
- `LexicalSyntacticFeaturizer`
- `RegexEntityExtractor`
- `CountVectorsFeaturizer`
- `DIETClassifier`
- `EntitySynonymMapper`
- `FallbackClassifier`

The policies include:
- `MemoizationPolicy`
- `RulePolicy`
- `TEDPolicy`

## Testing and Results

The project includes both **Rasa evaluation** and **general system testing**.

### Rasa Evaluation
The report presents the following metrics:

|        Task        | Accuracy | F1-Score | Precision |
|--------------------|----------|----------|-----------|
| Intent Recognition | 0.873    | 0.867    | 0.873     |
| Entity Recognition | 0.981    | 0.955    | 0.952     |

These results indicate strong performance in both intent classification and entity extraction.

### General Tests
The system was also tested for:
- person engagement
- head position reset
- arm movement
- response to being called
- microphone deactivation while Pepper is speaking

These tests confirmed the correct behavior of the main interaction modules.
