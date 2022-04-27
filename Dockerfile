FROM jupyter/minimal-notebook

WORKDIR /home/jovyan
RUN git clone https://github.com/liuxr98/jupytermagic-mysql.git
WORKDIR /home/jovyan/jupytermagic-mysql
RUN python3 setup.py bdist_wheel && pip install dist/mysqlmagic-1.0.0-py3-none-any.whl
WORKDIR /home/jovyan