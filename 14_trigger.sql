CREATE TRIGGER tgrCheckOperationCount
ON tblOperation INSTEAD OF INSERT
AS
	DECLARE @idOperType int, @idAccount int, @summa decimal, @data date, @operCount int;
	DECLARE InsCursor CURSOR FOR SELECT intOperationTypeId, intAccountId, fltValue, datOperation FROM inserted;
BEGIN
	OPEN InsCursor;
	FETCH NEXT FROM InsCursor INTO @idOperType, @idAccount,@summa,@data;

	WHILE @@FETCH_STATUS=0
		BEGIN
--			SET @idAccount=(SELECT distinct tblOperation.intAccountId
--							FROM tblOperation
--							WHERE tbl)
			SET @operCount=0;
			SET @operCount=(SELECT count(*)
							from tblOperation
							WHERE (intAccountId=@idAccount)
							AND (datOperation= @data))
			if(@operCount=0) INSERT INTO tblOperation(intOperationTypeId, intAccountId,fltValue,datOperation) 
							values(@idOperType,@idAccount, @summa,@data);
			FETCH NEXT FROM InsCursor INTO @idOperType,@idAccount, @summa,@data;
		END;
	CLOSE InsCursor;
	DEALLOCATE InsCursor;
END;
	