# user-service

[![codecov](https://codecov.io/gh/Xaril/user-service/branch/main/graph/badge.svg?token=BNKIZX5CI7)](https://codecov.io/gh/Xaril/user-service)
![Tests](https://github.com/xaril/user-service/actions/workflows/test.yaml/badge.svg)

This repository contains a [FastAPI](https://fastapi.tiangolo.com/) backend for creating and managing users. It uses [SQLModel](https://sqlmodel.tiangolo.com/) to handle database models and DTOs, and [injector](https://pypi.org/project/injector/) to more fully create a SOLID codebase.

The intended use of this service is as a complement to other services, such that they do not need to manage users themselves. Furthermore, this allows for multiple products to have the same user base.
