-- MySQL Workbench Forward Engineering

if object_id('dbo.yourtable') is not null
begin
  drop table dbo.yourtable
end

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MD5` DEFAULT CHARACTER SET utf8 ;
USE `MD5` ;

-- -----------------------------------------------------
-- Table `mydb`.`incidents`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`incidents` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `priority` INT NOT NULL,
  `resolved` TINYINT(1) NOT NULL DEFAULT 0,
  `category` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW(),
  `location` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`calls`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`calls` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `audio_path` TEXT NULL,
  `raw_text` TEXT NULL,
  `parsed_text` TEXT NULL,
  `location` VARCHAR(255) NULL,
  `incident_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_calls_incidents_idx` (`incident_id` ASC),
  CONSTRAINT `fk_calls_incidents`
    FOREIGN KEY (`incident_id`)
    REFERENCES `mydb`.`incidents` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
