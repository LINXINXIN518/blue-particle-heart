# Blue Particle Heart 蓝色粒子之心

A Python/Pygame desktop animation that forms a blue 3D particle heart from thousands of animated particles.

> 中文简介：这是一个使用 Python 和 Pygame 制作的蓝色粒子爱心动画项目。粒子从底部圆盘逐渐飞向画面中央，并组成一个具有 3D 旋转感的蓝色爱心。

## Preview 预览

![Blue Particle Heart Preview](assets/preview.png)

## Demo 动态演示

![Blue Particle Heart Demo](assets/preview.gif)

MP4 version: [`assets/preview.mp4`](assets/preview.mp4)

## Features 特性

- Generates a blue 3D heart using thousands of animated particles.
- Builds the heart from a rotating particle disk at the bottom of the screen.
- Uses perspective projection to create a 3D rotation effect.
- Includes floating, flying, and final-arrival particle states.
- Runs as a lightweight desktop animation with Pygame.
- Supports closing the window normally or pressing `Esc` to exit.

## Tech Stack 技术栈

- Python
- Pygame

## Requirements 环境要求

Recommended environment:

- Python 3.9 or later
- Pygame

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run 运行方式

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

## Project Structure 项目结构

```text
blue-particle-heart/
├── assets/
│   ├── preview.png      # Static preview image
│   ├── preview.gif      # Animated demo for README
│   └── preview.mp4      # MP4 demo version
├── main.py              # Main animation program
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Files ignored by Git
```

## Notes 说明

This is a Python/Pygame desktop project, not a web project. It cannot be deployed directly with GitHub Pages unless it is rewritten as a browser-based version using HTML/CSS/JavaScript, Canvas, WebGL, or Three.js.

The `build/`, `dist/`, executable files, cache files, and compressed packages are intentionally excluded from the repository to keep the project clean and source-code focused.

## Author 作者

Created by [LINXINXIN518](https://github.com/LINXINXIN518).
