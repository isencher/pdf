实体：
楼盘(Project), 楼栋(Building), 房产(Property), 户型(HouseType), 参与方(Party), 自然人(Person), 法人(Entity), 联系方式(Contact), 地址(Address), 客户(Customer), 销售顾问(SalesAdvisor), 员工(Employee), 交易(Transaction), 意向(Intention), 认购(Subscription), 签约(Signature), 按揭(Mortgage), 银行(Bank), 交房(Deliver), 计算应收(CalculateReceivable), 收款(Payment), 应收名目(ReceivableCategory), 用户(User), 角色(Role), 用户的角色(UserRole), 权限(Permission), 角色的权限(RolePermission), 资源(Resource), 权限的资源(PermissionResource)
约束：
1. 一个楼盘有多个楼栋，一个楼栋属于一个楼盘
2. 一个楼栋有多套房产, 一套房产属于一个楼栋
3. 一个户型对应多个房产，一个房产对应一个户型
4. 参与方可以是自然人或法人
5. 客户、员工、销售顾问都属于参与方
6. 一个参与方可以有多个联系方式，一个联系方式属于一个参与方
7. 一个参与方可以有多个地址，一个地址属于一个参与方
8. 交易可以是意向、认购、签约、按揭、交房
9. 一个客户可以产生多笔交易，一笔交易可以对应多个客户
10. 一个销售顾问可以产生多笔交易，一笔交易可以对应一个销售顾问
11. 一个房产可以对应多笔交易，一笔交易对应一个房产
12. 一个交易可以产生多笔计算应收，一笔计算应收对应一个交易
13. 一笔计算应收可以对应多笔收款，一笔收款对应一笔计算应收
14. 一个用户对应多名角色，一个角色对应多名用户
15. 一个角色对应多名权限，一个权限对应多名角色
16. 一个资源对应多名权限，一个权限对应多名资源

