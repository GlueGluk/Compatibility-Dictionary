Инструкция по запуску
Шаг 1. Скачивание документов
Перед запуском необходимо:
	* Установить MySQL (с сайта https://dev.mysql.com/downloads/installer/ для Windows), python3, pdftotext, uniconv, antiword; возможно, потребуются также какие-то библиотеи для python3
	(Установка библиотек:
		BeautifulSoup - pip install bs4
		pymysql - pip install pymysql
		lxml - pip install lxml
		
	* Создать базу данных MySQL под названием websites, дать к ней доступ пользователю с логином "testuser" и паролем "test123"
		(В консоли после установки MySQL набрать команду:
			mysql -u root -p
		Потребуется ввод пароля, по умолчанию он пустой.
		Вы окажетесь в консоли MySQL. Нужно ввести команды
			CREATE DATABASE websites;
			CREATE USER 'testuser'@'localhost';
			GRANT ALL PRIVILEGES ON websites.* To 'testuser'@'localhost' IDENTIFIED BY 'test123';
		)
	* В базе создать следующие таблицы (в скобках указаны необходимые столбцы)):
	 	 seen (name varchar(1000)) 
		 loaded (name varchar(1000), link varchar(500))
		 (Для этого оставаясь в консоли MySQL ввести команды
			USE websites;
			CREATE TABLE seen (name varchar(1000));
			CREATE TABLE loaded (name varchar(1000), link varchar(500));
		)
	* В файл sites.txt записать все сайты, которые хотите обойти
Запуск: python load_pdf.py (python3 load_pdf.py для ОС Linux)
Результат: будет создана папка library, в ней будут созданы папки для каждого обойденного сайта, в которые будут сохранены файлы в формате pdf, doc или docx, хранящиеся на этих сайтах.

Шаг 2. Конвертация в txt
Перед запуском необходимо:
    + Для Linux:
        * В текущем каталоге иметь папку library, в подпапках которой лежат документы для обработки
        * Дать права на исполнение файлу ba.sh (команда chmod +x ba.sh)
    Далее запустить ./ba.sh
    + Для Windows:
        * Установить LibreOffice (https://ru.libreoffice.org/download)
        * Добавить в PATH поддиректорию program директории, куда был установлен LibreOffice
            Пример: setx path "%path%;C:\Program Files (x86)\LibreOffice\program"
        * Загрузить XPdf (http://www.xpdfreader.com/download.html), извлечь из архива утилиту pdftotext.exe и проследить, чтобы путь к ней также находился в PATH.
    Запустить windows_make_txt.py
Результат: будет создана папка textfiles, в которую будет сохранено содержимое всех подпапок в library, конвертированное в формат txt (в случае, если конвертация возможна).
Опционально: для обработки текстов - удаления дефисов и фильтрации текстов, состоящих из двух колонок (переноса их в подпапку unprocessable) запустить python3 filter.py 

Шаг 3. Применение шаблонов. 
(У меня получилось только под Windows из-за особенностей lspl-find)
Перед запуском необходимо:
	* В текущем каталоге иметь папку textfiles, в которой лежат текстовые файлы, к которым нужно применять шаблоны.
	* В текущем каталоге иметь файлы pattens.txt и pattern\_names.txt в кодировке windows-1251; в файле patterns.txt - список всех шаблонов, в файле pattern\_names.txt - имена шаблонов из patterns.txt, которые нужно применить к коллекции текстов.
	* В текущий каталог в поддиректорию lspl распаковать архив lspl.zip.
	* Создать переменную окружения RML, в которую записать путь к поддиректории data в каталоге lspl текущей директории (команда вида setx RML "C:\Users\.....\Compatibility-Dictionary\lspl\data")
	* Скачать perl (например, отсюда http://strawberryperl.com), загрузить необходимую библиотеку для него - команда:
		cpan install Encode::Detect::Detector
	* Подготовить файлы к сопоставлению с шаблонами, запустив скрипт python conv_all.py
Запуск: python3 get_context.py

Шаг 4. Подсчет статистики и получение результатов.
Перед запуском необходимо:
    * Запустить скрипт, подготавливающий данные для быстрой работы приложения python prepare_interface_data.py
    * Установить библиотеку PyQt5 командой pip install PyQt5
Запуск: python interface.py