--Создайте триггер, который при удалении операции изменяет 
--значение поля «сумма на счете». Проверьте работу триггера.
CREATE TRIGGER tgr_tblOperation_delete
ON tblOperation AFTER DELETE
AS
	DECLARE @operTypeId int, @accId int, @sum decimal, @data date
	DECLARE intCursor cursor for Select intOperationTypeId, intAccountId,fltValue, datOperation
					FROM deleted
BEGIN
	OPEN intCursor 
	fetch from intCursor into @operTypeId,@accId, @sum, @data
	while @@FETCH_STATUS=0 
	BEGIN
		UPDATE tblAccount
		SET fltAccountSum = fltAccountSum-@sum
		WHERE tblAccount.intAccountId=@accId
		fetch from intCursor into @operTypeId,@accId, @sum, @data
		END;
	CLOSE intCursor;
	DEALLOCATE intCursor;
END
