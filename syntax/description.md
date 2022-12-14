## Устройство машины Тьюринга
* Бесконечная в обе стороны лента, разделенная на ячейки.
* Управляющее устройство, способное писать / читать из ячеек ленты, находящеесе в одном из множества состояний.
* Заранее заданный конечный алфавит, символы которого находятся в ячейках ленты; содержит пустой символ.
* Заранее заданное конечное множество состояний управляющего устройства; содержит начальное состояние и конечное состояние, определяющее завершение программы.
* Заранее заданный конечный набор правил перехода, по которым работает управляющее устройство; в зависимости от текущего состояния и символа в ячейке правило определяет действие записи / чтения для управляющего устройства и его дальнейшее перемещение вправо / влево.

## Синтаксис
Программа для машины Тьюринга состоит из определения алфавита, множества состояний и множества правил.  
Все символы алфавита заключены в `''`, за исключением `_`, обозначающего пустой символ.  
Все состояния это `$` + последовательность цифр, кроме конечного. `$0` начальное состояние, `$!` конечное состояние.  
Алфавит задается конструкцией `Alphabet(...)`, где в скобках перечислены символы, разделенные `,` .  Обязательно содержит `_`.
Множество состояний задается конструкцией `States(...)`, где в скобках перечислены состояния, разделенные `,` . Обязательно содержит `$0` и `$!`.    
Правило записывается как `(CUR_STATE, CUR_SYMBOL) -> (NEW_SYMBOL, MOVE, NEW_STATE)`, где `CUR_STATE` текущее состояние управляющего устройства, `CUR_SYMBOL` - символ в ячейке под управляющим устройством, `NEW_SYMBOL` - символ, который будет записан в текущую ячейку, `MOVE` - L / R - направление движения управляющего устройства после записи, `NEW_STATE` - новое состояние УУ после записи. Каждый из параметров правой части может быть указан как `None`, тогда соответствующее изменение не произойдет. Для каждого значения левой части может быть задано не более одного значения правой. Нельзя использовать конечное состояние в левой части.  
Комментарии однострочные, экранируются символом `#`.

## Примеры
В папке `examples`.  
`abstring.txt` - добавление в конец строки в алфавите `{'a', 'b'}` символа `a`.  
`plusone.txt` - прибавление к числу в двоичной записи 1.
