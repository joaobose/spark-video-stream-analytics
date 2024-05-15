# Spark video stream analytics

Python implementation of the Spark video stream analytics project. The original project was implemented in Java and can be found [here](https://github.com/baghelamit/video-stream-analytics/tree/master).

## Python environment setup

First, make sure you have a Python environment set up. You can use the following command to create a new environment:

```bash
python3 -m venv ./venv
```

Then source the enviroment with the following command:

```bash
source venv/bin/activate
```

Finally, install the required packages with the following command:

```bash
python3 -m pip install -r requirements.txt
```

Make sure to deactivate the environment when you are done with the following command:

```bash
deactivate
```

Whenever you want to work on the project, make sure to source the environment before running the code.


# Execution

## Motion detection demo

To run the motion detection demo, first source the environment:

```bash
source venv/bin/activate
```

Then run the following command:

```bash
python src/motion-demo.py
```