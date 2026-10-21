# 05-试题六：Java 面向对象程序设计（设计模式代码填空）

> **题型使命与通关战略**：下午试题六固定考查 Java 设计模式代码填空。满分 15 分，目标保底 **13 ~ 15 分**（全卷性价比最高大题！）。
> 核心抓手在于：
> 1. **UML 类图与 Java 代码 1:1 物理映射**：
>    - 组合/聚合菱形箭头指向谁，持有者的成员变量就是谁的引用类型；
>    - 虚线三角对应 `implements`，实线三角对应 `extends`；
> 2. **多态与委托调用核心三部曲**：接口/父类引用接收子类实例、运行时多态派发、委托回调传递 `this` 指针；
> 3. **Java 方法声明三要素**：访问修饰符（`public`/`protected`）、返回值类型（`void`/具体对象类型）、方法名与参数列表。

---

## 📅 历年真题复盘时间轴与实战对账表

| 考试年份与考次 | 试题背景与业务领域 | 核心考点与命题陷阱 | 错题编号与直达锚点 |
| :--- | :--- | :--- | :---: |
| **2019 年 5 月** | 汽车竞速游戏刹车痕迹 | 策略模式接口引用类型与委托调用 | [⭐ 案例错题 01](#case-2019-05-q6) |
| **2020 年 11 月** | 电商支付接口整合 | 中介者模式 Mediator、同事类解耦与双向引用满分典范 | [⭐ 案例错题 02](#case-2020-11-q6) |
| **2021 年 5 月** | 层叠菜单 | 组合模式Composite、UML井号符号映射protected与容器多态持有 | [⭐ 案例错题 03](#case-2021-05-q6) |
| **2021 年 11 月** | 网络围棋程序 | 享元模式Flyweight、内部状态与外部状态分离、单词拼写致命翻车血泪教训 | [⭐ 案例错题 04](#case-2021-11-q6) |
| **2022 年 5 月** | 备忘录模式 | 状态快照暂存、恢复与方法声明返回值类型遗漏 | [⭐ 案例错题 05](#case-2022-05-q6) |
| **2022 年 11 月** | 医院就医接待系统 | 外观模式Facade、接口方法声明与门面委托满分典范 | [⭐ 案例错题 06](#case-2022-11-q6) |
| **2023 年 5 月** | 区间显示格式 | 策略模式 Strategy 接口抽象、委托调用 this 与多态实例化满分典范 | [⭐ 案例错题 07](#case-2023-05-q6) |

---

## 🎯 历年真题实战错题深度透析

<a id="case-2019-05-q6"></a>
### ⭐ 案例错题 01：2019年5月试题六（汽车竞速游戏刹车痕迹——策略模式接口引用类型与委托调用） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：汽车竞速游戏，模拟长轮胎和短轮胎刹车痕迹，后续支持更多轮胎。采用策略模式（Strategy Pattern）实现。类图给出 `Car` 组合 `BrakeBehavior` 接口，两个具体刹车类 `LongWheelBrake` 与 `ShortWheelBrake` 实现接口。
> - **问题设问**：将应填入 (1) ~ (5) 处的字句写在答题纸的对应栏内（15分，每空3分）。
> - **考生现场作答与估分**：
>   - (1)：`void stop()` ✔（命中，得 3 分）
>   - (2)：`Car` ❌（致命混淆！Context 错写为自身，应为策略接口 `BrakeBehavior`，丢 3 分）
>   - (3)：`this.wheel.stop()` ✔（命中，得 3 分）
>   - (4)：`this.wheel = behavior` ✔（命中，得 3 分）
>   - (5)：`brake()` ✔（命中，得 3 分）
>   - *总分诊断*：得 12 分 / 满分 15 分（整体表现达 80% 优秀水平，但核心的策略接口引用类型失分非常可惜）。

* **【作答诊断与根因定性】**：
  * 🎯 **标准答案**：
    - `(1) void stop()`
    - `(2) BrakeBehavior`
    - `(3) wheel.stop()`（或 `this.wheel.stop()`）
    - `(4) wheel = behavior`（或 `this.wheel = behavior`）
    - `(5) brake()`
  * 💥 **三大致命翻车根因**：
    1. **【策略模式组合引用类型混淆（核心硬伤）】**：
       - 在策略模式中，Context（环境上下文角色 `Car`）为了解耦算法，必须持有一个**抽象策略接口类型的引用**（即 `BrakeBehavior wheel`），以便在运行时动态多态替换不同轮胎！
       - 考生错写为 `Car`，导致 `Car` 内部持有了另一个 `Car wheel`，完全违背了面向对象的组合逻辑，更无法调用 `wheel.stop()`！
    2. **【类图与代码 1:1 映射直觉缺失】**：
       - 在类图 5-1 中，`Car` 身上连出一条**实心菱形组合箭头，指向 `BrakeBehavior`**。
       - **UML 翻译成 Java 代码的铁律**：类图中的菱形关联线，**100% 对应类中的“成员变量”**！菱形端是持有者（`Car`），箭头端就是变量的类型（`BrakeBehavior`）！
    3. **【构造器参数类型反推探针失察】**：
       - 查看下文子类构造函数：`public ShortWheelCar(BrakeBehavior behavior) { this.wheel = behavior; }`
       - 形参 `behavior` 的声明类型是 `BrakeBehavior`，它被直接赋给了 `wheel`。
       - 根据 Java 强类型赋值兼容性，`wheel` 的声明类型必然是 `BrakeBehavior`！

* **【15秒秒杀与破局流水线（策略模式填空五大条件反射）】**：
  * **第一步：看实现类反推接口（秒杀空 1）**
    - 实现类写着 `class LongWheelBrake implements BrakeBehavior { public void stop() { ... } }`；
    - 接口里必然声明该方法原型 $\implies$ 1:1 照抄 `void stop()`！
  * **第二步：看类图菱形箭头定成员变量类型（秒杀空 2）**
    - 类图 `Car` 组合 `BrakeBehavior` $\implies$ `Car` 内部必有 `protected BrakeBehavior wheel;`。
  * **第三步：多态委托调用（秒杀空 3）**
    - `Car` 的 `brake()` 方法不需要自己实现刹车细节，直接甩手委托给策略对象 $\implies$ `wheel.stop();`。
  * **第四步：构造注入绑定（秒杀空 4）**
    - 外部传入策略对象 `behavior`，存入父类继承来的受保护字段 $\implies$ `this.wheel = behavior;`。
  * **第五步：客户端高层调用（秒杀空 5）**
    - `car1` 是汽车对象，业务需求是刹车，调用汽车暴露的高层业务接口 $\implies$ `car1.brake();`。

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **实现方法看接口，签名抄来不带体；**  
    > **类图菱形指接口，Context 持有策略型；**  
    > **环境高层不干活，多态委托 wheel 调 stop；**  
    > **构造传入赋成员，客户端只调高层 brake！**
  * **答题规范模板**：
    - 接口方法声明：`返回类型 方法名(形参)`，末尾不带大括号。
    - 组合成员变量：必须是接口或抽象类类型，实现面向接口编程。

---

<a id="case-2020-11-q6"></a>
### ⭐ 案例错题 02：2020年11月试题六（电商支付接口整合——中介者模式 Mediator、同事类解耦与双向引用满分典范） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：在线支付是电子商务的一个重要环节，不同的电子商务平台提供了不同的支付接口。现在需要整合不同电子商务平台的支付接口，使得客户在不同平台上购物时，不需要关心具体的支付接口。拟采用中介者（Mediator）设计模式来实现该需求，所设计的类图如图 6-1 所示。
> - **Java 核心代码框架**：
>   ```java
>   import java.util.*;
>   
>   interface WebServiceMediator {
>       public void __(1)__;
>       public void SetAmazon(WebService amazon);
>       public void SetEbay(WebService ebay);
>   }
>   
>   abstract class WebService {
>       protected __(2)__ mediator;
>       public abstract void SetMediator(WebServiceMediator mediator);
>       public __(3)__;
>       public abstract void search(double money);
>   }
>   
>   class ConcreteServiceMediator implements WebServiceMediator {
>       private WebService amazon;
>       private WebService ebay;
>       public ConcreteServiceMediator() {
>           amazon = null;
>           ebay = null;
>       }
>       public void SetAmazon(WebService amazon) { this.amazon = amazon; }
>       public void SetEbay(WebService ebay) { this.ebay = ebay; }
>       public void buy(double money, WebService service) {
>           if (service == amazon) amazon.search(money);
>           else ebay.search(money);
>       }
>   }
>   
>   class Amazon extends WebService {
>       public void SetMediator(WebServiceMediator mediator) { this.mediator = mediator; }
>       public void buyService(double money) {
>           __(4)__;
>       }
>       public void search(double money) { System.out.println("Amazon receive:" + money); }
>   }
>   
>   class Ebay extends WebService {
>       public void SetMediator(WebServiceMediator mediator) { this.mediator = mediator; }
>       public void buyService(double money) {
>           __(5)__;
>       }
>       public void search(double money) { System.out.println("Amazon receive:" + money); }
>   }
>   ```
> - **问题设问与考生实际作答**：
>   - **【问题1】（15分，每空3分）** 填充 Java 代码中的空 (1) ~ (5)。
>     - 空 (1)：`buy（double money，WebService service）` $\to$ **3.0 / 3.0 分（满分命中！）**
>     - 空 (2)：`WebServiceMediator` $\to$ **3.0 / 3.0 分（满分命中！）**
>     - 空 (3)：`abstract void buyService（double money）` $\to$ **3.0 / 3.0 分（满分命中！）**
>     - 空 (4)：`this.mediator.buy（money，this）` $\to$ **3.0 / 3.0 分（满分命中！）**
>     - 空 (5)：`this.mediator.buy（money，this）` $\to$ **3.0 / 3.0 分（满分命中！）**
>   - *【试题六全卷总分结算】*：实得 **15.0 / 15.0 分（100% 满分超神！）**！

* **【作答诊断与根因定性】**：
  * 🎯 **官方标准采分点**：
    - `(1) buy(double money, WebService service)`
    - `(2) WebServiceMediator`
    - `(3) abstract void buyService(double money)`
    - `(4) mediator.buy(money, this)`（或 `this.mediator.buy(money, this)`）
    - `(5) mediator.buy(money, this)`（或 `this.mediator.buy(money, this)`）
  * 💥 **中介者模式（Mediator Pattern）硬核技术本质**：
    1. **【解耦核心：网状拓扑化为星型拓扑】**：
       - 如果各个电商平台（Amazon、Ebay）之间直接相互依赖调用，系统耦合度将呈 $O(n^2)$ 爆炸；
       - 中介者模式引入一个中介者对象（Mediator），各个平台（同事类 Colleague）不再直接沟通，而是统一与中介者通信，将网状结构梳理为清爽的星型结构。
    2. **【双向引用与委托分发机制】**：
       - **中介者持同事**：`ConcreteServiceMediator` 内部维护了 `private WebService amazon, ebay;`；
       - **同事类持中介**：抽象基类 `WebService` 内部持有 `protected WebServiceMediator mediator;`；
       - **委托触发**：当同事类执行购买 `buyService(money)` 时，绝不自作主张，而是将控制权转交给中介者：`mediator.buy(money, this)`，将自身指针（`this`）传递过去，中介者根据传入的对象身份执行条件路由（`if (service == amazon) ...`）。
    3. **【考场满分亮点】**：
       - 考生 5 空无一失手！空 1 方法签名严格与实现类对齐，空 2 接口类型精准，空 3 抽象方法声明完整，空 4/5 准确使用 `this` 指针作为回调凭据，展现了极强的面向对象设计模式代码体感。

* **【15秒秒杀与破局流水线（中介者模式解题三步法）】**：
  * **第一步：看实现反推接口签名（秒杀空 1）**
    - 查实现类 `ConcreteServiceMediator`：有 `public void buy(double money, WebService service)`；
    - 接口中必然声明相同原型 $\implies$ 直接照抄为 **`buy(double money, WebService service)`**！
  * **第二步：看 Setter 与泛化定类型（秒杀空 2 与空 3）**
    - 查属性设值器：`SetMediator(WebServiceMediator mediator)` $\implies$ 空 2 变量类型必为 **`WebServiceMediator`**；
    - 查子类实现：Amazon 与 Ebay 均有 `public void buyService(double money)` $\implies$ 父类必有对应抽象方法 **`abstract void buyService(double money)`**！
  * **第三步：同事类向中介者汇报并交出 this（秒杀空 4 与空 5）**
    - 同事类调中介者的 `buy` 方法，参数需要金额和来源服务 $\implies$ 必填 **`this.mediator.buy(money, this)`**！

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **中介网状变星型，同事之间不直连；**  
    > **中介持有各同事，同事基类持中介；**  
    > **业务动作调中介，把自己 this 传过去；**  
    > **实现方法查接口，签名类型一字齐！**

---

<a id="case-2021-05-q6"></a>
### ⭐ 案例错题 03：2021年5月试题六（层叠菜单——组合模式Composite、UML井号符号映射protected与容器多态持有） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：层叠菜单是窗口风格系统中常用的一种功能组织方式。层叠菜单中包含的可能是一个菜单项（直接对应某个功能），也可能是一个子菜单。现在采用组合（Composite）设计模式实现层叠菜单。
>   - 系统给出类图 6-2：
>     - 抽象构件：`MenuComponent`，包含属性 `# name: String`，方法 `printName()`，抽象方法 `addMenuElement`、`removeMenuElement`、`getElement`；
>     - 叶子构件：`MenuItem` 继承 `MenuComponent`；
>     - 容器构件：`Menu` 继承 `MenuComponent`，内部组合包含 `elementList`。
>   - Java 代码实现层叠菜单的构建与遍历。
> - **设问小题与考生现场实际作答**：
>   - **代码填空 (1) ~ (5)**（15分，每空3分）：
>     - (1)：`private` ❌（官方标准为 `protected`，丢 3 分）
>     - (2)：`abstract boolean addMenuElement(MenuComponent element);` ✔（命中，得 3 分）
>     - (3)：`abstract List<MenuComponent> getElement();` ✔（命中，得 3 分）
>     - (4)：`List<MenuComponent> elementList` ✔（命中，得 3 分）
>     - (5)：`mainMenu.addMenuElement(subMenu);` ✔（命中，得 3 分）
>   - *【试题六全卷总分】*：实得 **12.0 分 / 15.0 分**（得分率 **80.0%**，设计模式理解极深，代码多态架构全通！）。

* **【作答诊断与根因定性】**：
  * 🎯 **标准答案**：
    - `(1) protected`
    - `(2) abstract boolean addMenuElement(MenuComponent element)`（或带分号）
    - `(3) abstract List<MenuComponent> getElement()`（或带分号）
    - `(4) ArrayList<MenuComponent> elementList;`（或 `List<MenuComponent> elementList;`）
    - `(5) mainMenu.addMenuElement(subMenu);`
  * 💥 **三大核心题眼与深层病理分析**：
    1. **【UML 可见性符号映射 Java 权限修饰符（空 1 丢分核心）】**：
       - 考生习惯性认为类的属性应当封装为 `private`，落入日常业务肌肉记忆；
       - 但在 UML 标准与软考考纲中：
         - `+` 对应 `public`（公共）
         - `-` 对应 `private`（私有）
         - `#` 对应 `protected`（受保护）
         - `~` 对应 `default`（包级私有）
       - 类图 6-2 中 `MenuComponent` 属性明确标注为 `# name`，考查点正是将 `#` 准确翻译为 Java 关键字 **`protected`**！
    2. **【代码反推验证：子类直访父类字段的语法约束】**：
       - 观察子类 `MenuItem` 构造器：`public MenuItem(String name) { this.name = name; }`；
       - 观察子类 `Menu` 构造器：`public Menu(String name) { this.name = name; ... }`；
       - 在 Java 中，若父类属性声明为 `private`，子类必须通过 `super(name)` 调用父类构造器，而绝不能直接使用 `this.name = name;`（编译直接报错：`name has private access in MenuComponent`）！
       - 只有当父类属性为 `protected` 时，子类才能合法直访继承而来的 `name` 字段！
    3. **【面向对象接口一致性与组合模式本质（空 2、3、4 满分技巧）】**：
       - **空 (2) & 空 (3)**：父类中已经给出了 `public abstract boolean removeMenuElement(MenuComponent element);`，对照子类重写的另外两个同名方法，补上 `abstract` 即可 100% 满分命中。
       - **空 (4)**：容器类 `Menu` 组合持有的子菜单项列表，既能装普通菜单项 `MenuItem`，也能装子菜单 `Menu`，容器类型必须为它们的共同抽象基类 `List<MenuComponent>`，完美达成树形递归组合！

* **【15秒秒杀与破局流水线（组合模式与修饰符定位三步法）】**：
  * **第一步：看类图符号定修饰符（秒杀空 1）**
    - 见加号写 public，见减号写 private，见井号 `#` 必填 **`protected`**！
    - 子类直写 `this.name` 反向双重印证 protected！
  * **第二步：看子类实现补抽象声明（秒杀空 2 与空 3）**
    - 找到子类公共方法，父类补齐 `public abstract <返回类型> <方法名>(<参数>)`！
  * **第三步：容器构件持有抽象基类集合（秒杀空 4 与空 5）**
    - `List<MenuComponent> elementList` 实现多态容纳；
    - 主菜单装入子菜单 $\implies$ `mainMenu.addMenuElement(subMenu);`！

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **加公减私井保护，符号映射莫含糊！**  
    > **子类直写 this.name，私有 private 报编译；**  
    > **组合模式树形套，容器持有构件表；**  
    > **主单加入子菜单，addMenuElement 调调调！**
  * **答题规范模板**：
    - UML 权限映射：见到 `#` 绝不写 private，必写 `protected`。
    - 组合模式容器：`List<抽象构件> 变量名` 或 `ArrayList<抽象构件> 变量名`。

---

<a id="case-2021-11-q6"></a>
### ⭐ 案例错题 04：2021年11月试题六（网络围棋程序——享元模式Flyweight、内部状态与外部状态分离、单词拼写致命翻车血泪教训） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：享元模式(Flyweight)主要用于减少创建对象的数量，以降低内存占用，提高性能。现开发一个网络围棋程序，允许多个玩家联机下棋。由于只有一台服务器，为节省内存空间，采用享元模式实现该程序。
>   - 系统给出类图 6-1：`PieceBoard` 包含棋子列表；`Piece`（抽象类）泛化具体子类 `BlackPiece` 和 `WhitePiece`；`Piece` 关联 `PiecePos`（棋子坐标）。
>   - 代码框架：
>     - `PiecePos` 封装外部状态：位置坐标 `x, y`。
>     - `Piece` 抽象享元基类：保护成员 `m_color`（内部状态颜色）和 `m_pos`（外部状态位置），构造函数 `Piece(PieceColor, PiecePos)`，抽象方法 (1)。
>     - `BlackPiece` / `WhitePiece` 具体享元类：继承 `Piece`，实现 `public void draw()` 绘制棋子。
>     - `PieceBoard` 棋盘客户端：静态列表 (2) `m_arrayPiece` 保存已有棋子；方法 `SetPiece(PieceColor, PiecePos)` 声明局部变量 (3) `piece = null`，根据颜色分支实例化后分别调用 (4)、(5) 绘制落子，并加入列表。
> - **问题设问**：将应填入 (1) ~ (5) 处的字句写在答题纸的对应栏内（15分，每空3分）。
> - **考生现场作答与估分**：
>   - (1)：`abstract public void draw();` ✔（逻辑语法完全正确，题干后方自带分号，多写分号属极轻微格式瑕疵，实得 3.0 分）
>   - (2)：`Price` ❌（致命拼写手误！把棋子 `Piece` 误拼为价格 `Price`，多了字母 `r`，类型未定义）
>   - (3)：`Price` ❌（致命拼写手误！把 `Piece` 误拼为 `Price`，类型未定义）
>   - (4)：`price.draw()` ⚠️（致命拼写手误！代码中变量名为 `piece`，考生写为 `price.draw()`）
>   - (5)：`price.draw()` ⚠️（致命拼写手误！同上）
>   - $\implies$ *【试题六全卷总分】*：
>     - **面向对象设计与逻辑思维**：15.0 / 15 分（5 个空全部命中设计模式考点，泛型、多态、抽象方法、调用时机全通！）；
>     - **代码精确性与拼写灾难**：因单词手滑多写了一个字母 `r`（`Piece -> Price`），导致 4 个空连环受创！
>     - *严格编译器阅卷*：实得 **3.0 分 / 15 分**（白丢 12 分巨款！惨烈至极！）；
>     - *人工通融阅卷*：实得 **6.0 ~ 7.5 分 / 15 分**。

* **【作答诊断与根因定性】**：
  * 🎯 **标准答案**：
    - `(1) public abstract void draw()`（或 `protected abstract void draw()`）
    - `(2) Piece`
    - `(3) Piece`
    - `(4) piece.draw()`
    - `(5) piece.draw()`
  * 💥 **三大核心题眼与认知破局**：
    1. **【软考代码填空最高警戒天条：抄写单词绝不盲打，1:1 字面核对】**：
       - 为什么全盘把 `Piece` 写成了 `Price`？
         - **肌肉记忆惯性陷阱**：在日常业务开发中，程序员打 `price`（价格）的频次远高于 `piece`（棋子/碎片），手指敲击键盘时下意识滑入了 `p-r-i-c-e` 的肌肉记忆。
         - **考场保命铁律**：**试题六填空的所有类名与变量名，100% 都在题干说明、类图和已有代码中明文出现！**
           - 类图 6-1 赫然印着：`Piece`；
           - 抽象类声明明文写着：`abstract class Piece`；
           - 局部变量初始化明文写着：`piece = null;`；
           - 只要在答卷时强迫自己**“抬头看题干，一个字母一个字母对齐抄写（P-i-e-c-e）”**，就能 100% 规避这种让 12 分瞬间灰飞烟灭的灭顶之灾！
    2. **【享元模式（Flyweight）精髓：内部状态与外部状态彻底分离】**：
       - 围棋盘有 $19 \times 19 = 361$ 个交叉点，上万玩家同时联机。如果每个落子都 `new` 一个独立对象，单台服务器的堆内存瞬间爆仓 OOM！
       - **享元化改造机制**：
         - **内部状态（Intrinsic State）**：可以跨对象高度共享、不可变的内在属性 $\implies$ **棋子颜色（PieceColor BLACK / WHITE）**！全系统其实只需共享 2 个享元对象！
         - **外部状态（Extrinsic State）**：随落子场景动态变化、不可共享的属性 $\implies$ **棋子坐标位置（PiecePos x, y）**！
         - 外部状态不存入享元对象核心，而是在绘制或计算时由客户端外部传入，从而实现“成千上万棋子落盘，内存仅耗两颗对象”的极限性能！
    3. **【面向对象容器泛型与多态引用（空2、空3、空4、空5逻辑复盘）】**：
       - 空(2) 容器泛型：`ArrayList<Piece>`。棋盘存放的棋子既有黑子也有白子，容器必须声明为它们的共同基类 `Piece`，实现面向接口/抽象类编程。
       - 空(3) 引用声明：`Piece piece = null;`。先定义父类统一引用，在 `if-else` 分支中分别指向 `BlackPiece` 或 `WhitePiece` 具体实例。
       - 空(4)、空(5) 多态调用：无论实例化的是哪种颜色子类，统一利用多态机制调用 `piece.draw()` 触发对应子类的绘制行为。考生逻辑全对，败于单词手滑！

* **【15秒秒杀与破局流水线】**：
  * **第一步：看子类实现，秒杀父类抽象声明（秒杀空1）**
    - 子类 `BlackPiece` 和 `WhitePiece` 均有 `public void draw()` $\implies$ 父类必有对应抽象方法 `public abstract void draw();`（注意原题已有分号）。
  * **第二步：看集合多态，秒杀泛型类型（秒杀空2）**
    - `ArrayList<...>` 存棋盘所有棋子 $\implies$ 必须填抽象父类 `Piece`！
  * **第三步：看分支实例化，秒杀引用类型（秒杀空3）**
    - 分支里 `piece = new BlackPiece(...)` $\implies$ 统一引用的静态声明类型必是 `Piece`！
  * **第四步：看落子后动作，秒杀方法调用（秒杀空4与空5）**
    - 打印了落子位置后，必须进行界面呈现 $\implies$ 调用 `piece.draw();`！
  * **第五步：防翻车终极质检——单词字符逐一核对！**
    - 检查空(2)~(5)的所有单词拼写，对照题干 `Piece`，坚决剔除多余的 `r`！

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **享元设计省内存，内部颜色外部位；**  
    > **子类共性抽抽象，父类声明带 void；**  
    > **容器声明看基类，多态调用 draw 绘棋；**  
    > **最怕手滑多写 r，字字核对 P-I-E-C-E！**
  * **答题规范模板**：

---

<a id="case-2022-05-q6"></a>
### ⭐ 案例错题 05：2022年5月试题六（备忘录模式——状态快照暂存、恢复与方法声明返回值类型遗漏） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：软件系统中提供取消或撤销错误操作的选择，允许系统恢复到原先状态。采用备忘录（Memento）模式实现。类图 6-1 包含三大角色：
>   - `Originator`（原发器/发起人）：创建并在 Memento 中存储状态；
>   - `Memento`（备忘录）：存储发起人的内部状态；
>   - `CareTaker`（管理者/负责人）：负责从 Memento 恢复状态，维护历史列表 `mementoList`。
> - **问题设问**：阅读说明和 Java 代码，将应填入 (1) ~ (6) 处的字句写在答题纸的对应栏内（15分，每空2.5分）。
> - **考生现场作答与估分**：
>   - **【代码填空作答】（15分，每空2.5分）**：
>     - 空(1)：`new Memento(this.state)` ✔（命中！`this.state` 等价于 `state`，得 2.5 分）；
>     - 空(2)：`memento.getState()` ✔（命中！得 2.5 分）；
>     - 空(3)：`add(Memento state)` ⚠️/❌（**全场唯一失分点**：题干前面只有 `public`，漏写返回类型 `void` 导致语法非法，严苛判 0 分，宽容得 1.0 分）；
>     - 空(4)：`Memento get(int Index)` ✔（命中！形参大小写不影响语义，得 2.5 分）；
>     - 空(5)：`originator.saveStateToMemento()` ✔（命中！得 2.5 分）；
>     - 空(6)：`originator.saveStateToMemento()` ✔（命中！得 2.5 分）；
>     - $\to$ *小计 12.5 ~ 13.5 分 / 15 分*（基准稳健估分 **12.5 分**，得分率高达 83.3% 🌟 极高分拿盘！）。
>   - *【试题六全卷总分】*：实得 **12.5 分 / 满分 15 分**（面向对象与 Java 语法基本功极其扎实！）。

* **【作答诊断与根因定性】**：
  * 🎯 **标准答案**：
    - `(1) new Memento(state)`（或 `new Memento(this.state)`）
    - `(2) memento.getState()`
    - `(3) void add(Memento state)`
    - `(4) Memento get(int index)`（或 `Memento get(int Index)`）
    - `(5) originator.saveStateToMemento()`
    - `(6) originator.saveStateToMemento()`
  * 💥 **三大致命翻车根因（空3为什么必带 `void`？）**：
    1. **【Java 方法签名语法三要素缺失（致命隐蔽陷阱）】**：
       - Java 中普通方法的定义语法为：`[修饰符] <返回类型> <方法名>(<形参列表>)`。
       - 审视题干原代码：
         ```java
         public (3) {
             mementoList.add(state);
         }
         ```
         题干的空 (3) 位于 `public` 和 `{` 之间。如果只填 `add(Memento state)`，由于缺少返回类型，Java 编译器会强制将其视为构造函数；但方法名为 `add`，与类名 `CareTaker` 不匹配，编译器直接报错：`invalid method declaration; return type required`！
       - 因为添加操作无需返回值，必须显式声明返回类型为 **`void`**（即 `void add(Memento state)`）！
    2. **【下文调用反推形参类型意识（空3与空4）】**：
       - 观察主函数：`careTaker.add(originator.saveStateToMemento())`，而 `saveStateToMemento()` 返回的是 `Memento` 对象；因此 `add` 方法的形参必须声明为 `Memento state`。
       - 观察下文：`originator.getStateFromMemento(careTaker.get(0))`，而 `getStateFromMemento` 接收 `Memento`；且方法体内执行 `return mementoList.get(index)`，因此 `get` 的返回类型必为 `Memento`，形参为 `int index`！
    3. **【快照暂存与恢复调用闭环（空5与空6）】**：
       - 主函数在修改状态前后调用 `careTaker.add(...)` 保存快照，显然传入的是发起人生成的备忘录对象 `originator.saveStateToMemento()`。考生两空均精准命中！

* **【15秒秒杀与破局流水线（备忘录模式秒杀心法）】**：
  * **第一步：看类图定三大角色权责**
    - `Originator`（发起人）：拥有内部状态 `state`，负责生产备忘录（`saveStateToMemento`）和从备忘录恢复（`getStateFromMemento`）。
    - `Memento`（备忘录）：存储特定时刻的快照状态，只提供只读 getter（`getState`）。
    - `CareTaker`（负责人）：只管按列表存取备忘录（`add` / `get`），不能也不应修改备忘录内容。
  * **第二步：秒杀快照生成与恢复（空1、空2）**
    - 生成快照：`return new Memento(state);`（将当前状态打包进新备忘录）。
    - 恢复快照：`state = memento.getState();`（从备忘录取回状态赋给自身成员）。
  * **第三步：补全管理者方法签名（空3、空4，重点查返回类型）**
    - 盯住空前面的单词：如果是 `public (3) {`，绝不能只写方法名，必须带上返回类型！
    - 添加无返回值 $\implies$ **`void add(Memento state)`**；
    - 查询返回 Memento $\implies$ **`Memento get(int index)`**。
  * **第四步：主函数调用（空5、空6）**
    - `careTaker.add(...)` 的入参必须是一个 `Memento` 对象，由发起人生产 $\implies$ **`originator.saveStateToMemento()`**！

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **备忘录里藏状态，发起人员造快照；**  
    > **存进 new 个 Memento，恢复调取 getState；**  
    > **管理容器只管存，方法签名莫漏 void；**  
    > **存前调用 saveState，两处保存一字同！**
  * **答题规范模板**：
    - 方法头填空：必须完整包含 `<返回类型> <方法名>(<形参列表>)`，切忌漏写 `void`！
    - 创建备忘录：`new Memento(state)` 或 `new Memento(this.state)`。

---

<a id="case-2022-11-q6"></a>
### ⭐ 案例错题 06：2022年11月试题六（医院就医接待系统——外观模式Facade、接口方法声明与门面委托满分典范） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：Facade（外观/门面）模式通过为多个复杂子系统提供一致的接口，使子系统更易访问。以医院为例，患者需与挂号（Registry）、门诊（Doctor）、取药（Pharmacy）等部门交互。为简化流程，设置接待员（Facade），代患者完成就医步骤。类图给出 Patient 接口与其实现类 ConcretePatient，Disposer 接口与其三个实现类，以及门面类 Facade。
> - **设问小题与考生现场实际作答**：
>   - **Java 代码填空 (1) ~ (6)**（15分，每空2.5分）：
>     - 空 (1)：`public String getName()` $\implies$ **2.5 / 2.5 分（满分命中！）**
>     - 空 (2)：`public void dispose(Patient patient)` $\implies$ **2.5 / 2.5 分（满分命中！）**
>     - 空 (3)：`new ConcretePatient(args[0])` $\implies$ **2.5 / 2.5 分（满分命中！）**
>     - 空 (4)：`Facade` $\implies$ **2.5 / 2.5 分（满分命中！）**
>     - 空 (5)：`new Facade(patient)` $\implies$ **2.5 / 2.5 分（满分命中！）**
>     - 空 (6)：`f.dispose()` $\implies$ **2.5 / 2.5 分（满分命中！）**
>   - *【试题六全卷总分结算】*：实得 **15.0 / 15.0 分（🏆 100% 满分超神神卷！）**！

* **【作答诊断与根因定性】**：
  * 🎯 **官方标准采分点**：
    - `(1) String getName()` 或 `public String getName()`
    - `(2) void dispose(Patient patient)` 或 `public void dispose(Patient patient)`
    - `(3) new ConcretePatient("name")` 或 `new ConcretePatient(args[0])` 或 `new ConcretePatient("xxx")`
    - `(4) Facade`
    - `(5) new Facade(patient)`
    - `(6) f.dispose()`
  * 🌟 **外观模式（Facade Pattern）硬核技术本质与满分亮点**：
    1. **【接口一致性推导法（空 1 与空 2）】**：
       - `ConcretePatient` 实现了 `Patient` 接口，内部有 `public String getName() { return name; }`，因此接口 `Patient` 内部必须声明 `public String getName()`；
       - `Registry`、`Doctor`、`Pharmacy` 实现了 `Disposer` 接口，内部均有 `public void dispose(Patient patient)`，因此接口 `Disposer` 内部必须声明 `public void dispose(Patient patient)`；
    2. **【客户端解耦与接待员门面调用（空 3~6）】**：
       - 客户端 `FacadeTest` 无需直接依赖繁杂的子系统对象（挂号处、医生、药房），只需初始化就诊患者 `patient = new ConcretePatient(args[0])`，交给接待员门面 `Facade f = new Facade(patient)`，最后一条指令触发全流程 `f.dispose()`；
       - 考生 6 空无一失手，尤其在空 3 灵活使用 `args[0]` 接收主函数入参，代码规范度和工程直觉无可挑剔！

* **【15秒秒杀与破局流水线】**：
  * **第一步：看实现反推接口抽象方法（秒杀空 1 与空 2）**
    - 照抄实现类的公共方法签名，去掉方法体大括号即可。
  * **第二步：创建被接待业务实体（秒杀空 3）**
    - 构造实现类 `new ConcretePatient(args[0])`。
  * **第三步：创建门面外观对象并委托执行（秒杀空 4~6）**
    - 门面类型 `Facade`，带参构造 `new Facade(patient)`，最后调用统一门面方法 `f.dispose()`。

* **【机考实战防坑口诀与答题规范模板】**：
  * **避坑口诀**：  
    > **外观模式建门面，统一接口解耦连；**  
    > **接口方法看实现，参数返回照样填；**

---

<a id="case-2023-05-q6"></a>
### ⭐ 案例错题 07：2023年5月试题六（区间显示格式——策略模式 Strategy 接口抽象、委托调用 this 与多态实例化满分典范） 【🔥重点标星】

> **【真题背景与设问回溯】**
> - **试题背景**：在某系统中，类 `Interval` 代表由下界（lower bound）和上界（upper bound）定义的区间。要求采用不同的格式显示区间范围（如 `[lower,upper]`、`[lower...upper]`、`[lower-upper]` 等），采用策略（Strategy）模式实现。
>   - 包含枚举 `TYPE { COMMA, DOTS, LINE }`；
>   - 策略接口 `PrintStrategy`；
>   - 上下文类 `Interval` 持有 `lower` 和 `upper`，提供 `printIntervals(PrintStrategy ptr)`；
>   - 具体策略类 `PrintIntervalsComma`、`PrintIntervalsDots`、`PrintIntervalsLine` 分别实现不同格式打印；
>   - `Main.getStrategy(TYPE type)` 根据枚举类型创建并返回对应策略对象。
> - **问题设问与考生实际作答**：
>   - **【代码填空】（15分，每空3分）** 填充 Java 代码中的空 (1) ~ (5)。
>     - 空 (1)：`void doPrint(Interval val)` $\implies$ **3.0 / 3.0 分（满分全中！）**
>     - 空 (2)：`ptr.doPrint(this)` $\implies$ **3.0 / 3.0 分（满分全中！）**
>     - 空 (3)：`st = new PrintIntervalsComma()` $\implies$ **3.0 / 3.0 分（满分全中！）**
>     - 空 (4)：`st = new PrintIntervalsDots()` $\implies$ **3.0 / 3.0 分（满分全中！）**
>     - 空 (5)：`st = new PrintIntervalsLine()` $\implies$ **3.0 / 3.0 分（满分全中！）**
>   - *【试题六全题总分结算】*：实得 **15.0 / 15.0 分（满分全中！神级表现！）**！

* **【满分典范解构与技术本质】**：
  * 🎯 **官方标准采分点**：
    - `(1) void doPrint(Interval val)`
    - `(2) ptr.doPrint(this)`
    - `(3) st = new PrintIntervalsComma()`
    - `(4) st = new PrintIntervalsDots()`
    - `(5) st = new PrintIntervalsLine()`
  * 💥 **策略模式（Strategy Pattern）核心运转机理**：
    1. **【抽象策略接口定义（空 1）】**：
       - 查看实现类：三大实现类均声明 `public void doPrint(Interval val)`；
       - 接口内天然具有 `public` 修饰，填空只需补齐方法返回类型、方法名与形参列表：`void doPrint(Interval val)`。
    2. **【上下文委托与 this 穿透（空 2）】**：
       - `Interval` 类调用策略对象的打印行为：`printIntervals(PrintStrategy ptr)`；
       - `ptr` 调用的方法是 `doPrint`，需要接收一个 `Interval` 类型的实例；
       - 当前正处于 `Interval` 内部方法中，代表当前区间对象自身的是关键字 `this`，因此精准写出 **`ptr.doPrint(this)`**，实现完美解耦与委托！
    3. **【多态实例简单工厂分支（空 3~5）】**：
       - 在 `switch(type)` 中根据枚举选择具体策略，将实例赋值给局部变量 `st`；
       - 对应分支分别为 `new PrintIntervalsComma()`、`new PrintIntervalsDots()`、`new PrintIntervalsLine()`，语法工整，单词拼写零失误。

* **【机考实战防坑指南】**：
  * **防坑口诀**：  
    > **策略接口看实现，方法签名照着抄；**  
    > **环境委派调策略，当前对象传 this；**  
    > **多态分支 new 策略，类型对应不能差！**

---

---

## 🛡️ 本题型命题人扣分红线与标准化答题模板

1. **关键字全小写铁律**：Java 关键字如 `null`、`this`、`return`、`void`、`new` 必须全小写，首字母大写直接零分。
2. **方法签名严防漏写返回值类型**：如接口方法声明 `public void update();`，绝不可遗漏 `void`。
3. **设计模式核心类名单词核对**：如 `Flyweight`、`Composite`、`Mediator`、`Strategy`、`Memento`，逐字母对齐，防止手滑。
