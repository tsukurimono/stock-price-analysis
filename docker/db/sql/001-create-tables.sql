DROP TABLE IF EXISTS `candlesticks`;
DROP TABLE IF EXISTS `tags`;
DROP TABLE IF EXISTS `stocks_tags`;
DROP TABLE IF EXISTS `delistings`;

create table IF not exists `candlesticks`
(
 `code`       VARCHAR(20)  NOT NULL,
 `market`     VARCHAR(20)  NOT NULL,
 `date`       DATE NOT NULL,
 `open`       DECIMAL(20,7) NOT NULL,
 `close`      DECIMAL(20,7) NOT NULL,
 `high`       DECIMAL(20,7) NOT NULL,
 `low`        DECIMAL(20,7) NOT NULL,
 `volume`     INT(20) NOT NULL,
 `patched`    BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (`code`, `market`, `date`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

create table IF not exists `delistings` like `candlesticks`;

create table IF not exists `tags`
(
 `id`         INT NOT NULL AUTO_INCREMENT,
 `name`       VARCHAR(256)  NOT NULL,
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

create table IF not exists `stocks_tags`
(
 `code`         VARCHAR(20) NOT NULL,
 `market`       VARCHAR(20) NOT NULL,
 `tag_id`       INT NOT NULL,
    PRIMARY KEY (`code`, `market`, `tag_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
