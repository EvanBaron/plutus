{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: [ ps.pip ]))
  ];

  shellHook = ''
    if [ -L .venv ]; then rm .venv; fi

    if [ ! -d .venv ]; then
      echo "Creating virtual environment..."
      python -m venv .venv
    fi

    source .venv/bin/activate

    export PIP_USER=0
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet

    echo "Environment ready!"
  '';
}
