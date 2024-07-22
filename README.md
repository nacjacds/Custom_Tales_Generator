![Header Image](assets/header.png)

# Custom Tales Generator

## Introduction

This is a custom tales generator using the OpenAI API, LangChain, FastAPI, Docker, and an AWS database.

## Application Functionality

The user selects one of the two available languages, enters a name for the protagonist of the story, adds one or more characters, describes the scenario or situation for the story, chooses the story length (short, medium, or long), and clicks the "Generate Story" button.

Once the story is generated, voice controls appear, allowing the user to read the story aloud, pause, resume, or stop the narration to create a new story.

All generated stories are stored in an AWS database along with the user queries used to create them.

## Tools and Technologies

The following tools and languages were used to create this application:

- **OpenAI API**: Used to generate custom stories based on user input such as the child's name, characters, and scenarios.
- **LangChain**: Employed to enhance the quality and relevance of the language model's responses.
- **FastAPI**: Used for integration with other tools and to handle the application's backend functionalities.
- **Docker**: Utilised to package the application, making it deployable on any platform.
- **AWS Database**: Stores user queries and generated stories.
- **Text-to-Speech**: Leverages the capabilities of modern browsers to read stories aloud, with controls for play, pause, resume, and stop.

## Usage

1. Select a language (English or Spanish).
2. Enter the protagonist's name.
3. Add characters and describe the scenario.
4. Choose the length of the story (short, medium, or long).
5. Click "Generate Story".
6. Use the voice controls to read, pause, resume, or stop the story.

All user inputs and generated stories are stored in an AWS database for future reference.
## Check this video to see how it works:
<a href="https://www.loom.com/share/4094c8b19942443a891532e494d21755?sid=9c93ed3a-08a9-4259-9ae9-6fd24e2551ef" target="_blank">Custom Tales Generator Video</a>

## Docker
<a href="https://hub.docker.com/repository/docker/nacjacds/custom_tales/general" target="_blank">Docker Hub Repository</a>
