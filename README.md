# Sanfoundry MCQ Saver
### Saves all the mcqs in pdf file and also merges them.

# Steps to run:

1. Install required libraries:

    ```
    pip install -r requirements.txt
    ```
2. Install wkhtmltopdf:

    - Windows

      Use binary installer, download from [here](https://wkhtmltopdf.org/downloads.html)

      OR

      If [Chocolatey](https://chocolatey.org/) is installed
      ```
      choco install wkhtmltopdf
      ```

    - Debian/Ubuntu

      ```
      sudo apt-get install wkhtmltopdf
      ```
    - macOS
    
      ```
      brew install homebrew/cask/wkhtmltopdf
      ```
3. Run the script
    ```
    python sanfoundry.py
    ```

Script uses below types of link.

For downloading single mcq page.

![Single MCQ SET](https://github.com/falcon883/Sanfoundry-MCQ-Saver/blob/main/images/single_link.PNG)

For downloading all mcq sets.

![Multiple MCQ SET](https://github.com/falcon883/Sanfoundry-MCQ-Saver/blob/main/images/multi_link.PNG)


You can also use these types of link (Program Examples):

Program Sets: https://www.sanfoundry.com/c-programming-examples-stacks/

Single Programs: https://www.sanfoundry.com/c-program-stack-implementation/

## Contributions 
All contributions are welcome, as long as they are meaningful.

## Contributors
<a href="https://github.com/falcon883/Sanfoundry-MCQ-Saver/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=falcon883/Sanfoundry-MCQ-Saver" />
</a>

Made with [contributors-img](https://contrib.rocks).
