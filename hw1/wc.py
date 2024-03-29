import click
import sys


def wc_calc(text):
    """Function to calc statistics for text files like wc Linux utility.
    It calcs and returns for some input text file numbers of lines,
    numbers of words and numbers of bytes or symbols.

    Parameters
    ----------
    text : str
        text from text file or stdin to process.

    Returns
    -------
    lines_cnt: int
        numbers of lines in text file
    words_cnt: int
        words of lines in text file
    symbols_cnt: int
        symbols of lines in text file
    """
    lines_cnt, words_cnt, symbols_cnt = 0, 0, 0

    for line in text:
        lines_cnt += 1
        words_cnt += len(line.split())
        symbols_cnt += len(line)

    return lines_cnt, words_cnt, symbols_cnt


def read_text_file(file_path):
    """Function to read all lines from txt file

    Parameters
    ----------
    file_path : str
        The path to the text file to process.

    Returns
    -------
    lines : list
        list of lines from text file.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    return lines


def wc_print(wc_data, n):
    """Function to print statistics for text files like wc Linux
    utility output

    Parameters
    ----------
    wc_data : list
        wc_data presented in form of list of list like
        [[line_cnt_str_1, word_cnt_str_1, symbols_cnt_str_1, text_file_path_1],
        ...
        [line_cnt_str_n, word_cnt_str_n, symbols_cnt_str_n, text_file_path_n],
        ]
    n : int
        the number of characters occupied by the largest number in the wc statistics.
        It used for good formatting similar to wc Linux utility output
    """
    for line in wc_data:
        lines_cnt, words_cnt, symbols_cnt, file = line
        line = (
            f"{lines_cnt.rjust(n)} "
            f"{words_cnt.rjust(n)} "
            f"{symbols_cnt.rjust(n)} "
            f"{file}"
        )
        print(line)


@click.command()
@click.option("--file_path", "-f", multiple=True)
def wc_func(file_path):
    """Simple function that works like `nl -b a` Linux utility

    Parameters
    ----------
    file_path : str
        The path to the text file to process.
    """
    if file_path:
        if len(file_path) == 1:
            text = read_text_file(file_path[0])
            lines_cnt, words_cnt, symbols_cnt = wc_calc(text)
            print(f"{lines_cnt} {words_cnt} {symbols_cnt} {file_path[0]}")
        else:
            wc_output_data = []
            total = [0, 0, 0]

            for file in file_path:
                text = read_text_file(file)
                result_wc_calc = wc_calc(text)

                # считаем total
                result_wc_calc = list(result_wc_calc)
                total = [sum(i) for i in zip(total, result_wc_calc)]

                # добавляем строку данные для вывода
                result_wc_calc = [str(i) for i in result_wc_calc]
                result_wc_calc.append(file)
                wc_output_data.append(result_wc_calc)

            n = len(str(max(total)))
            total.append("total")
            wc_output_data.append([str(i) for i in total])

            wc_print(wc_output_data, n)

    else:
        # считываем stdin
        text = []
        for line in sys.stdin:
            text.append(line)

        total = wc_calc(text)
        total = ["\t" + str(i) for i in total]
        total = "".join(total)
        print(total)


if __name__ == "__main__":
    wc_func()
