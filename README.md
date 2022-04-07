# Python CLI Application Template

## usage
### generate a key card stl
```
encrypt_3d --key 123 generate-key --key-output example/key.stl
```


### generate a key card stl
encodes an image, note that you MUST use the same key
```
encrypt_3d --key 123 encode --image-input example/oshw.png --image-output example/oshw.stl
```

### optional parameters
number of holes on x axis
```
--grid-width
```

number of holes on y axis
```
--grid-height
```

size of holes (in range 0-1, as ratio to pixel size)
```
--hole-ratio
```

## development setup

- create a virtual env
- install project editable: `pip install -e ".[dev]"`
- install commit hooks: `pre-commit install`

### run all checks
```
pre-commit run --all-files
```
### run specific checks
```
pre-commit run --all-files [HOOK_ID]
```

check `.pre-commit-config.yaml` for `HOOK_ID`

## build
```
python -m build
```
wheels will be in `dist` folder
