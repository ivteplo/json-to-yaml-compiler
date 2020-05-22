#/usr/bin/env bash
for f in Tests/*.json
do
    echo "Building $f to ${f%.json}.yaml"
    ./index.py "$f" --output ${f%.json}.yaml
done

