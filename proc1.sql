-- Создание процедуры
create procedure tblClosedAccounts
as
BEGIN
SELECT tblAccountType.txtAccountTypeName,tblAccount.txtAccountNumber, 
	tblAccount.datAccountBegin, tblAccount.datAccountEnd,

	tblClient.txtClientSurname,tblClient.txtClientName, 
	tblClient.txtClientSecondName,tblClient.txtClientAddress,

	tblOperation.datOperation, tblOperationType.txtOperationTypeName,
	tblOperation.fltValue

INTO #tempTblClosedAccounts
FROM tblAccount, tblAccountType, tblClient, 
	tblOperationType,tblOperation
WHERE (tblAccount.intClientId=tblClient.intClientId) AND
	(tblAccount.intAccountTypeId=tblAccountType.intAccountTypeId) AND
	(tblOperation.intOperationTypeId=tblOperationType.intOperationTypeId) AND
	(tblOperation.intAccountId=tblAccount.intAccountId)
ORDER BY txtAccountTypeName, txtAccountNumber, datOperation

select * from #tempTblClosedAccounts;
END

