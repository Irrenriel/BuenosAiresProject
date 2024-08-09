# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionContext
from core.redis_db import redis_db
from resources.response import PackageResponseModel, PackageCreateModel, PackageTypeResponseModel, \
    PackageTypeCreateModel
from resources.tables import PackageModel, PackageTypeModel

router = APIRouter()


@router.post(
    "/packages/create",
    response_model=PackageResponseModel,
    description="Create a new package",
)
async def create_package(package: PackageCreateModel, session: AsyncSession = Depends(SessionContext)):
    exchange_rate = await redis_db.get_exchange_rate()

    session.add(
        new_package := PackageModel(
            name=package.name,
            weight=package.weight,
            type_id=package.type_id,
            value=package.value,
            delivery_cost=PackageModel.get_delivery_cost(package.weight, package.value, exchange_rate),
        )
    )

    await session.commit()
    await session.refresh(new_package)

    return PackageResponseModel(
        id=new_package.id,
        name=new_package.name,
        weight=new_package.weight,
        type={'id': new_package.type.id, 'name': new_package.type.name},
        value=new_package.value,
        delivery_cost=new_package.delivery_cost,
    )


@router.post(
    '/types/create/',
    response_model=PackageTypeResponseModel,
    description="Create a new package type",
)
async def create_package_type(package_type: PackageTypeCreateModel, session: AsyncSession = Depends(SessionContext)):
    session.add(
        new_package_type := PackageTypeModel(
            name=package_type.name,
        )
    )

    await session.commit()
    await session.refresh(new_package_type)

    return PackageTypeResponseModel(
        id=new_package_type.id,
        name=new_package_type.name,
    )


@router.get(
    "/types",
    response_model=Page[PackageTypeResponseModel],
    description="List all available package types",
)
async def get_package_types(session: AsyncSession = Depends(SessionContext)):
    disable_installed_extensions_check()
    return paginate(
        [
            PackageTypeResponseModel(
                id=package_type.id,
                name=package_type.name
            ) for package_type in await PackageTypeModel.get_all(session)
        ]
    )


@router.get(
    "/packages/",
    response_model=Page[PackageResponseModel],
    description="List all available packages",
)
async def get_packages(session: AsyncSession = Depends(SessionContext)):
    disable_installed_extensions_check()
    return paginate(
        [
            PackageResponseModel(
                id=package.id,
                name=package.name,
                weight=package.weight,
                type={'id': package.type.id, 'name': package.type.name},
                value=package.value,
                delivery_cost=package.delivery_cost
            ) for package in await PackageModel.get_all(session)
        ]
    )


@router.get(
    "/package/{package_id}",
    response_model=PackageResponseModel,
    description="Get a specific package by `package_id`",
)
async def get_package(package_id: int, session: AsyncSession = Depends(SessionContext)):
    if not (package := await session.get(PackageModel, {'id': package_id})):
        raise HTTPException(status_code=404, detail="Package not found!")

    return PackageResponseModel(
        id=package.id,
        name=package.name,
        weight=package.weight,
        type={'id': package.type.id, 'name': package.type.name},
        value=package.value,
        delivery_cost=package.delivery_cost
    )


@router.post(
    "/exchange_rate/update",
    description="Trigger update costs for all packages",
)
async def update_packages_costs(session: AsyncSession = Depends(SessionContext)):
    if not (exchange_rate := await redis_db.get_exchange_rate()):
        raise HTTPException(status_code=404, detail="Exchange rate not available!")

    for package in await PackageModel.get_all(session):
        package.delivery_cost = PackageModel.get_delivery_cost(package.weight, package.value, exchange_rate)

    await session.commit()

    return {"status": "success"}
