# Storage Tracker
Author : CdRook
Description: backend API for tracking household storage. Keep track of what's in stock and how much is left.

Built with FastAPI, SQLModel, and SQLite. Deployed via Docker on a DigitalOcean VPS with automated CI/CD through GitHub Actions.

## Features

- Add, remove, and update products
- Automatic availability tracking (marks a product as absent when quantity hits 0)
- HTTPS in production via Let's Encrypt

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| GET | `/product/{name}` | Get a product by name |
| POST | `/add_product?product_name=&product_quantity=` | Add a new product |
| PATCH | `/update_product?product_name=&product_quantity=` | Update product quantity |
| DELETE | `/remove_product?product_name=` | Remove a product |

## Running Locally

**Prerequisites:** Docker Desktop

```bash
docker volume create storage_tracker_db
docker compose up --build
```

The API will be available at `http://localhost:8000`.

To seed the database with initial data:

```bash
poetry install
poetry run python scripts/seed_db.py
```

## Running Tests

```bash
pip install tox
tox -e py311    # tests + coverage
tox -e flake8   # linting
tox -e mypy     # type checking
```

## Deployment

Pushes to `main` automatically trigger the CI/CD pipeline:
1. Tests, linting, and type checking must pass
2. On success, the VPS pulls the latest code and rebuilds the Docker container

Pushes to `dev` run tests only — no deployment.



                                       ......................
                     ..:-+*%@@@@%%#*=-...    . . .............-=*#%%@@@@#*=-:..
                    -++*#%@@@@@@@%#*=:.                      .:=+#%@@@@@@@%#*+==
                      -%@*::::::::::::::::::::::::::::::::::::::::::-----=%@%-
                       -#@=:::::.........:::::::......:::::::::::::::----#@%-
                        .+#--::::........................:::::::::::----*@*:
                         .-*=-:::::......................:::::::::----=#%+.
                           .=+-::::::::......::::::::::.::::::::-----=#*:
                             .=--:::::::..::::::..:.::::::..::-----=+*-
                               .-----::.:::.:....:::...::::-::--==+=:
                                  .----=+=-::...:--:::::-=**=--==:.
                                    ..:::----=+******+=------::.
                                         ..-=----------=-..
                                           :#:        :*-
                                           :#:   ..   :#-
                                           :#=....:...-#-
                                       ..::---=+****+=---:...
                                    .:::::=#%*+++++*+*#%%=::::..
                                  .::::-%%+==============*@#-::::.
                                .:::::*@+::--:.:::-:::-----*@*::::.
                              .::::::#@=---...:..+#:.:...-=-=@#:::::.
                             .::::..=@+--...     -=     ..:=-+@=.::::.
                             ::::...*+--:.:-.    -=.    .=.---+*..::::.
                            :::....:....::..    -=.*.    ...::......:::
                           .:::....:. .....     .+*=      ..:. .:....::.
                           :::....::. .....    .......   ..... ::....:::
                           ::.....:::.  .:.-:=+.*+*+-:+.-.... .:::....::.
                           ::.....::::. @#--:.::.....:.::-#@ .::::....::.
                          .::....:::::::*@@@*=::.:.:::=*%@@*::::::....::.
                          .::.....::::::::=%@@@@@@@@@@@@@=::::::::....:::.
                          .-:.....:::::::::::::-=+==-:::::::::::::...::-:
                           .:--:::::::::::::::::::::::::::::::::::---=-:.
                           .....:::----======---------=========--:::....
                            ................::::::::::::::..............
                            ...........................................
                             .........................................
                              ..........                    .........
                                  .....                       ......

ASCII art generated with asciiart.eu
