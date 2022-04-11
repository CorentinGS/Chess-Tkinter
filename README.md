# Chess-Tkinter

## About it 

Chess-Tkinter is a school project

It's a simple chess game that allows you to play against an engine (stockfish by default).

## Missing 

- Working *en passant*
- Promotion 

## Known issues 

- Castling as black 

## Libraries 

### Tkinter

Tkinter was unfortunately required to be used for this project. 
It might be changed to QT if for some reason this project is maintained in the future.

### Numpy
Numpy is used to handle all the logic. It helps to use an array as the chess board because it's much easier to maintain and much faster and safer than native python list.

### Chess
Chess is used to handle the engine.

## Images
The project uses the following [images](https://commons.m.wikimedia.org/wiki/Category:SVG_chess_pieces) which are under Creative Commons license.

## Future 

This project was made as a school project. It won't be maintained.
However, I might rewrite it in the future in another lang as a learning purpose.

Otherwise, if you want to contribute feel free to open a pull request.

## Thanks 

- [TriForMine](https://github.com/TriForMine/py-chess-tk/) for the images and the project idea

# Installation

## Install python 3.10 

Install Conda to manage python env
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -p $HOME/miniconda3
```

Install python 3.10
```shell
conda create -n py310 python=3.10
conda activate py310
```

Install dependencies
```shell
pip install -r requirements.txt
```

Run it 
```shell
python3 __main__.py
```


