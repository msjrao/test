-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`d_browser`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`d_browser` ;

CREATE TABLE IF NOT EXISTS `mydb`.`d_browser` (
  `browser_id` INT NOT NULL,
  `browser_name` VARCHAR(50) NOT NULL,
  `major_browser` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`browser_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`d_user_agent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`d_user_agent` ;

CREATE TABLE IF NOT EXISTS `mydb`.`d_user_agent` (
  `user_agent_id` BIGINT NOT NULL,
  `user_agent` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`user_agent_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`d_referrer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`d_referrer` ;

CREATE TABLE IF NOT EXISTS `mydb`.`d_referrer` (
  `referrer_id` INT NOT NULL AUTO_INCREMENT,
  `referrer` VARCHAR(255) NOT NULL,
  `website` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`referrer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`d_os`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`d_os` ;

CREATE TABLE IF NOT EXISTS `mydb`.`d_os` (
  `operating_system_id` INT NOT NULL,
  `operating_system` VARCHAR(255) NULL,
  `major_os` VARCHAR(45) NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`operating_system_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`d_date`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`d_date` ;

CREATE TABLE IF NOT EXISTS `mydb`.`d_date` (
  `date_id` INT NOT NULL,
  `full_date` DATE NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`date_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`f_page_events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`f_page_events` ;

CREATE TABLE IF NOT EXISTS `mydb`.`f_page_events` (
  `trans_id` BIGINT NOT NULL,
  `visitor_id` INT NULL,
  `user_agent_id` BIGINT NOT NULL,
  `browser_id` INT NOT NULL,
  `operating_system_id` INT NOT NULL,
  `resolution_id` INT NULL,
  `hit_date_id` INT NULL,
  `visit_num` INT NULL,
  `page_event` INT NULL,
  `referrer_id` INT NOT NULL,
  `duration_on_page` INT NULL,
  `load_date` INT NULL,
  PRIMARY KEY (`trans_id`),
  INDEX `fk_browser_id_idx` (`browser_id` ASC),
  INDEX `fk_user_agent_id_idx` (`user_agent_id` ASC),
  INDEX `fk_referrer_id_idx` (`referrer_id` ASC),
  INDEX `fk_os_id_idx` (`operating_system_id` ASC),
  INDEX `fk_date_id_idx` (`hit_date_id` ASC),
  CONSTRAINT `fk_browser_id`
    FOREIGN KEY (`browser_id`)
    REFERENCES `mydb`.`d_browser` (`browser_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_agent_id`
    FOREIGN KEY (`user_agent_id`)
    REFERENCES `mydb`.`d_user_agent` (`user_agent_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_referrer_id`
    FOREIGN KEY (`referrer_id`)
    REFERENCES `mydb`.`d_referrer` (`referrer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_os_id`
    FOREIGN KEY (`operating_system_id`)
    REFERENCES `mydb`.`d_os` (`operating_system_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_date_id`
    FOREIGN KEY (`hit_date_id`)
    REFERENCES `mydb`.`d_date` (`date_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


insert into mydb.d_referrer values (0,'Unknown',null,now(),now());

insert into mydb.d_user_agent values (0,'Unknown',now(),now());


truncate table mydb.f_page_events;




