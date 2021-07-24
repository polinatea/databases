-- Создание процедуры
create procedure tblAccountStatement
@accNum CHAR(20)
as
BEGIN
SELECT tblAccountType.txtAccountTypeName, tblClient.txtClientSurname,
	tblClient.txtClientName, tblClient.txtClientSecondName,
	tblAccount.datAccountBegin,tblOperation.datOperation, 
	tblOperationType.txtOperationTypeName, tblOperation.fltValue
INTO #tempTblAccountsStatement
FROM tblAccountType, tblClient,tblAccount, 
	tblOperationType,tblOperation
WHERE (tblAccount.intClientId=tblClient.intClientId) AND
	(tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId) AND
	(tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND
	(tblOperation.intAccountId=tblAccount.intAccountId) AND
	(tblAccount.txtAccountNumber=@accNum)
ORDER BY datOperation DESC

SELECT * FROM #tempTblAccountsStatement;
END