# Neural Network Line Follower

## About
Code created for bachelor degree diploma project. The goal was to create a line follower robot steered by artificial neural network.

The neural network was trained using Deep Q-learning algorithm in a custom simulation environment created with `PyGame`. 
Then it was extracted to physical robot that uses Raspberry Pi as main computing unit.

------------------------

## Dependencies 
You don't really have to worry about it if you're using `pipenv` (and if you aren't you really *should be*).

Just run 
```
pipenv install
```
to create virtual environment with all the required packages listed in `Pipfile`.

Then start it using
```
pipenv shell
```
and now your development environment is ready.

For running tests make sure you have `RPi.GPIO` and `TensorFlow 2.3.0` installed on your Raspberry Pi.\
As installation of `TF 2.*` is not that simple on older models of RPi, I recommend reading this [guide](https://itnext.io/installing-tensorflow-2-3-0-for-raspberry-pi3-4-debian-buster-11447cb31fc4) to do so.

### Used packages
- [Pipenv](https://pypi.org/project/pipenv/)
- [Black](https://pypi.org/project/black/)
- [Flake8](https://pypi.org/project/flake8/)
- [isort](https://pypi.org/project/isort/)
- [NumPy](https://pypi.org/project/numpy/)
- [Pandas](https://pypi.org/project/pandas/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [PyGame](https://pypi.org/project/pygame/)
- [TensorFlow](https://pypi.org/project/tensorflow/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)

------------------------
