@echo off

for /R %%f in (*.png) do (
    echo %%f
    optipng %%f -strip all
)
