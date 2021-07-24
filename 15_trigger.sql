 --Создайте триггер, который при добавлении новой операции изменяет значение поля «сумма на 
--счете» (как изменяет?). Согласуйте данные в соответствующих таблицах для обеспечения 
--целостности базы данных. 

CREATE TRIGGER tgr_tblOperation_update
ON tblOperation AFTER INSERT
AS
	DECLARE @operTypeId int, @accId int, @sum decimal, @data date
	DECLARE intCursor cursor for Select intOperationTypeId, intAccountId,fltValue, datOperation
					FROM inserted
BEGIN
	OPEN intCursor 
	fetch from intCursor into @operTypeId,@accId, @sum, @data
	while @@FETCH_STATUS=0 
	BEGIN
		UPDATE tblAccount
		SET fltAccountSum = fltAccountSum+@sum
		WHERE tblAccount.intAccountId=@accId
		fetch from intCursor into @operTypeId,@accId, @sum, @data
		END;
	CLOSE intCursor;
	DEALLOCATE intCursor;
END
