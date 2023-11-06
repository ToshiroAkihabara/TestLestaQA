from wikipedia import WikiArticleTable, StorageTable, RowsTable
from engine2D import Engine2D
import time

def run_engine2D():
    engine = Engine2D()
    show_canvas = engine.show_canvas()
    change_color = engine.change_color_pencil()
    figures = [engine.add_circle(), engine.add_triangle(), engine.add_rectangle()]
    show_canvas = engine.show_canvas()
    draw_canvs = engine.draw()
    show_canvas = engine.show_canvas()

def run_engine_tests():
    """
    pytest tests/test_engine2d.py
    """
    pass
    
def run_wiki():
    wiki = WikiArticleTable()
    table: StorageTable = wiki.get_classobject(1)
    for i in table:
        i: RowsTable
        print(f"Столбец: {i.column_name} Значение: {i.column_item}")

def run_wiki_tests():
    """
    pytest tests/test_wiki.py
    """
    pass

def main():
    run_engine2D()
    time.sleep(3)
    run_wiki()
    
if __name__ == "__main__":
    main()