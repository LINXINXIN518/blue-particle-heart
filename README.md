# Blue Particle Heart

A Python/Pygame desktop animation that generates a blue 3D particle heart from a rotating particle disk.

> 中文简介：这是一个使用 Python 和 Pygame 制作的蓝色粒子爱心动画项目。粒子会从底部圆盘逐渐飞向画面中央，并组成一个旋转的 3D 爱心。

## Preview

Add a screenshot or demo GIF here after uploading the project.

```text
preview.gif or screenshot.png
```

## Features

- Generates a blue 3D heart using thousands of animated particles.
- Builds the heart from a rotating white particle disk at the bottom of the screen.
- Uses simple perspective projection to create a 3D rotation effect.
- Runs as a standalone desktop animation with Pygame.
- Supports exiting with the window close button or the `Esc` key.

## Tech Stack

- Python
- Pygame

## Requirements

Recommended environment:

- Python 3.9 or later
- Pygame

Install dependencies with:

```bash
pip install -r requirements.txt
```

## How to Run

Clone this repository:

```bash
git clone https://github.com/LINXINXIN518/blue-particle-heart.git
cd blue-particle-heart
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

## Project Structure

```text
blue-particle-heart/
├── main.py              # Main animation program
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Files ignored by Git
```

## Notes

This is a Python/Pygame desktop project, not a web project. It cannot be deployed directly with GitHub Pages unless it is rewritten as an HTML/CSS/JavaScript project.

If you want to publish a browser-based version later, the project should be rebuilt with technologies such as HTML, CSS, JavaScript, Canvas, WebGL, or Three.js.

## Author

Created by [LINXINXIN518](https://github.com/LINXINXIN518).
