DELIMITER $$

DROP PROCEDURE IF EXISTS addToken$$

CREATE PROCEDURE addToken(IN user VARCHAR(16), IN tok VARCHAR(128))

BEGIN

IF EXISTS
   (
   SELECT token
   FROM Users
   WHERE username = user AND
      token IS NOT NULL AND 
      (TIMESTAMP(NOW()) BETWEEN tokenTime AND TIMESTAMPADD(HOUR, 2, tokenTime))
   ) THEN
   SELECT token FROM Users WHERE username = user;

ELSE

START TRANSACTION;

   UPDATE Users
   SET
      token = tok,
      tokenTime = CURRENT_TIMESTAMP()
   WHERE
      username = user;
COMMIT;

SELECT token
   FROM Users
   WHERE
      username = user;

END IF;

END$$

DELIMITER ;
