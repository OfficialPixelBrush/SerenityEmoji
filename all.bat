@echo off

for %%f in (*.png) do (
  echo %%f
  optipng %%f -strip all 
)
