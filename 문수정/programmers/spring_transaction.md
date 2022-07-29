# 스프링 AOP와 트랜잭션

## AOP(Aspect Orient Programming)
- 관점 지향 프로그래밍
- 공통 관심사(cross cutting concern)
- 핵심기능과 부가기능을 분리
- 비즈니스 로직에 핵심적이지 않은 동작 추가

### 용어
- 타겟: aop 적용 대상, 핵심 기능 담고 있는 모듈
- 조인 포인트: aop 적용 위치, 타겟 객체가 구현한 인터페이스의 메서드
- 포인트 컷: 어디에 aop 적용할지 표현한 것(표현식)
    - @Pointcut("execution(public * com.example.order..*Service.*(..))")
- 애스펙트: 어드바이스 + 포인트 컷, Spring은 Aspect를 빈으로 등록
- 어드바이스(메서드)
    - 타겟의 특정 조인 포인트에 제공할 부가기능(aop)
    - @Before, @After, @Around, @AfterReturning, @AfterThrowing 등
- 위빙: 타겟의 조인 포인트에 어드바이스를 적용하는 과정(aop 적용)

### AOP 적용방법
- 컴파일 시점
- 클래스 로딩 시점
- **런타임 시점**
    - 스프링 제공방식
    - AOP Proxies
        - JDK Proxy(인터페이스)
        - CGLib Proxy(클래스)

### JDK Proxy

```java

    //InvocationHandler의 invoke를 구현한 클래스
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        //log 찍는 것을 앞에서 해주고 targer의 메소드를 실행시킴
        //add excuted in com.example.order.CalculatorImpl
        log.info("{} excuted in {}", method.getName(), targer.getClass().getCanonicalName());
        return method.invoke(targer, args);
    }

    @Test
    void JdkProxy() {
        //핸들러에는 실제 타겟이 될 객체 필요
        CalculatorImpl calculator = new CalculatorImpl();

        //Aop 구현 클래스와 적용할 인터페이스, 핸들러 전달
        //프록시 만들어짐
        Calculator proxyInstance = (Calculator) Proxy.newProxyInstance(
                LoggingInvocationHandler.class.getClassLoader(),
                new Class[]{Calculator.class},
                new LoggingInvocationHandler(calculator));

        //Handler의 invoke 실행 -> target 객체의 add() 실행
        int result = proxyInstance.add(1, 2);
        log.info("add->{}",result);//add->3
    }
```

## Spring AOP
aop dependency 추가
```
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-aop</artifactId>
    </dependency>
```
- AspectJ Annotation 이용
- 런타임에 적용

```java
    @Aspect //Aspect는 여러 어드바이스(메서드)를 담고있다
    @Component //빈으로 등록 되어야함
    public class LoggingAspect {

        private static final Logger log = LoggerFactory.getLogger(LoggingAspect.class);

        @Around("@annotation(com.example.order.aop.TrackTime)")//TrackTime annotation 붙은 메서드에만 적용
        public Object log(ProceedingJoinPoint joinPoint) throws Throwable {
            log.info("Before method called. {}", joinPoint.getSignature().toString());
            long startTime = System.nanoTime();
            Object result = joinPoint.proceed();
            long endTime = System.nanoTime() - startTime;
            log.info("After method called with result -> {} and time taken {} nanoseconds", result, endTime);
            return result;
        }
    }
```
advised 메서드 알려줌

## 트랜잭션
- 데이터베이스의 상태를 변경시키기 위해 수행하는 작업 단위
- 성공과 실패가 분명하고 상호 독립적
- 특징(ACID)
    - Atomicity(원자성): 트랜잭션이 데이터베이스에 모두 반영되던지, 아니면 전혀 반영 되지 않아야 함, 오류 발생시 트랜잭션 전부 취소
    - Consistency(일관성): 고정요소는 트랜잭션 수행 전과 수행 완료 후의 상태가 같아야 함
    - Isolation(독립성): 한 트랜잭션 완전히 종료될 때까지 다른 트랜잭션에서 수행 결과 참조 불가
    - Durability(지속성): 트랜잭션 성공시 결과 영구적
- Commit: 트랜잭션 성공했을 때 db 반영
- Rollback: 트랜잭션 처리 비정상적으로 종료 -> 모든 연산 취소

[트랜잭션(Transaction)이란? | ACID](https://code-lab1.tistory.com/51)


### TransactionManager
```java
public void testTransaction(Customer customer) {
        //트랜잭션 가져옴
        TransactionStatus transaction = transactionManager.getTransaction(new DefaultTransactionDefinition());
        try {
            jdbcTemplate.update("update customers set name = :name where customer_id = UUID_TO_BIN(:customerId)", toPramMap(customer));
            jdbcTemplate.update("update customers set email = :email where customer_id = UUID_TO_BIN(:customerId)", toPramMap(customer));
            //성공시 커밋
            transactionManager.commit(transaction);
        } catch (DataAccessException e) {
            //실패시 롤백
            logger.error("Got error", e);
            transactionManager.rollback(transaction);
        }
    }

    //Config파일에 bean등록
    @Bean
    public PlatformTransactionManager platformTransactionManager(DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
```

### transactionTemplate
```java
    public void testTransaction(Customer customer) {
            //리턴 결과 없을 때 TransactionCallbackWithoutResult
            //예외시 알아서 롤백처리
            transactionTemplate.execute(new TransactionCallbackWithoutResult() {
                @Override
                protected void doInTransactionWithoutResult(TransactionStatus status) {
                    jdbcTemplate.update("update customers set name = :name where customer_id = UUID_TO_BIN(:customerId)", toPramMap(customer));
                    jdbcTemplate.update("update customers set email = :email where customer_id = UUID_TO_BIN(:customerId)", toPramMap(customer));
                }
            });
        }
    
    //Config파일에 bean등록
    @Bean
    public TransactionTemplate transactionTemplate(PlatformTransactionManager platformTransactionManager) {
        return new TransactionTemplate(platformTransactionManager);
    }
```

### @Transactional
```java
//서비스에서 트랜잭션 로직 실행
@Transactional
public void createCustomers(List<Customer> customers) {
    customers.forEach(customerRepository::insert);
}

//Config파일에 @EnableTransactionManagement
```
