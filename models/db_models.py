from sqlalchemy import Column
from sqlalchemy import (DateTime, BigInteger, Text, ForeignKey, Integer, String,
                        Boolean, TIMESTAMP, Numeric, JSON, Date, Double)
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from datetime import datetime, date
from typing import Optional, List


# Создаем базовый класс для декларативного стиля SQLAlchemy,
class Base(DeclarativeBase):
    pass


# Модель таблицы "users"
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, primary_key=True, nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    registration_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=datetime.utcnow)
    temperature: Mapped[float | None] = mapped_column(Double, nullable=True)
    audio: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    speed: Mapped[float | None] = mapped_column(Double, nullable=True)
    current_tariff: Mapped[str | None] = mapped_column(
        String(50), nullable=True)
    subscription_start_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, default=date.today)
    subscription_end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, default=date.today)
    auto_renewal: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=True)
    card_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    card_last_digits: Mapped[str | None] = mapped_column(
        String(4), nullable=True)
    subscription_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2), nullable=True)
    subscription_duration: Mapped[int | None] = mapped_column(
        Integer, nullable=True)
    daily_message_count: Mapped[int | None] = mapped_column(
        Integer, nullable=True)
    last_reset_date: Mapped[datetime] = mapped_column(
        Date, nullable=True, default=date.today)
    promo_code: Mapped[str | None] = mapped_column(String(50), nullable=True)


# Модель таблицы "psychologists"
class Psychologist(Base):
    __tablename__ = 'psychologists'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле name - VARCHAR(255), необязательное
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # Поле description - TEXT, необязательное
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Поле avatar - VARCHAR(255), обязательное
    avatar: Mapped[str] = mapped_column(String(255), nullable=False)
    # Поле display_name - VARCHAR(255), обязательное
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Поле psychologist_name - TEXT, обязательное
    psychologist_name: Mapped[str] = mapped_column(Text, nullable=False)


# Модель таблицы "courses"
class Course(Base):
    __tablename__ = 'courses'
    # Поле course_id - INTEGER, первичный ключ
    course_id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле category - VARCHAR(255), обязательное
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    # Поле course_name - VARCHAR(255), обязательное
    course_name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Поле description - TEXT, обязательное
    description: Mapped[str] = mapped_column(Text, nullable=False)


# Модель таблицы "lessons"
class Lesson(Base):
    __tablename__ = 'lessons'
    # Поле block_id - INTEGER, первичный ключ
    block_id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле course_id - INTEGER, внешний ключ, обязательное
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('courses.course_id'), nullable=False)
    # Поле lesson_name - TEXT, обязательное
    lesson_name: Mapped[str] = mapped_column(Text, nullable=False)
    # Поле content - TEXT, обязательное
    content: Mapped[str] = mapped_column(Text, nullable=False)


# Модель таблицы "psy_messages"
class PsyMessages(Base):
    __tablename__ = 'psy_messages'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле user_id - BIGINT, внешний ключ, ссылается на таблицу users
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.user_id), nullable=False)
    # Поле day_time с типом DATETIME
    day_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime)
    # Поле psy_name - VARCHAR(50), обязательное
    psy_name: Mapped[str] = mapped_column(String(50), nullable=True)
    # Поле message - TEXT, необязательное
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


# Модель таблицы "lessons_messages"
class LessonsMessages(Base):
    __tablename__ = 'lessons_messages'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле user_id - BIGINT, внешний ключ, ссылается на таблицу users
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.user_id), nullable=False)
    # Поле day_time с типом DATETIME
    day_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime)
    # Поле course_id
    course_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # Поле block_id
    block_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # Поле message - TEXT, необязательное
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


# Модель таблицы "support_query"
class SupportQuery(Base):
    __tablename__ = 'support_query'
    # Поле id - INTEGER, первичный ключ
    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    # Поле user_id - BIGINT, внешний ключ, ссылается на таблицу users
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(User.user_id), nullable=False)
    # Поле day_time с типом DATETIME
    date_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime)
    # Поле message - TEXT, необязательное
    query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class PaymentRecord(Base):
    __tablename__ = "payment_records"
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(
        User.user_id), nullable=False)  # ID пользователя
    payment_id: Mapped[str] = mapped_column(
        String(255), nullable=False)  # Уникальный ID платежа
    status: Mapped[str] = mapped_column(
        String, nullable=False)  # Статус платежа
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False)  # Оплачен ли
    refundable: Mapped[bool] = mapped_column(
        Boolean, nullable=True)  # Возможность возврата

    # Поля для суммы платежа
    amount_value: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), nullable=True)  # Сумма платежа
    amount_currency: Mapped[str] = mapped_column(
        String, nullable=True)  # Валюта платежа

    # Поля для дохода
    income_amount_value: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), nullable=True)  # Сумма дохода
    income_amount_currency: Mapped[str] = mapped_column(
        String, nullable=True)  # Валюта дохода

    description: Mapped[str | None] = mapped_column(
        String, nullable=True)  # Описание
    payment_method: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Метод оплаты
    recipient: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Получатель
    authorization_details: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Авторизационные данные
    refunded_amount: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Данные о возврате
    metadata_payment: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Метаданные
    captured_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=datetime.utcnow)  # Дата завершения платежа (если оплачено)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True, default=datetime.utcnow)  # Дата создания платежа
    test: Mapped[bool] = mapped_column(
        Boolean, nullable=False)  # Тестовый режим
    confirmation: Mapped[dict | None] = mapped_column(
        JSON, nullable=True)  # Подтверждение (для неоплаченных)


# Модель таблицы История сообщений
class GPTHistory(Base):
    __tablename__ = 'gpt_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_bot_msg = Column(Boolean, nullable=False, default=False)
    message = Column(String, nullable=False)
