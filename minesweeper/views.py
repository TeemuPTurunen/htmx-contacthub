import random

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from enum import Enum, auto
import time
import queue

from .game_state import board, board_y, board_x, board_mines, clients_lock, clients, TileState  # import shared state

# tile = {
#     "state": TileState.HIDDEN_EMPTY,  # from the enum
#     "hovered_by": None,               # or player ID string
#     "highlight": False                # e.g. reveal area preview
# }

def index(request):
    # if "board" not in request.session:
    #     # Initialize fresh board
    #     board = [
    #         [{"state": TileState.HIDDEN_EMPTY.name, "hovered_by": None,
    #             "highlight": False} for _ in range(9)]
    #         for _ in range(9)
    #     ]
        
    #     all_positions = [(x, y) for x in range(9) for y in range(9)]
    #     bomb_positions = random.sample(all_positions, 33)
    #     print(f"Bomb positions: {bomb_positions}")

    #     for x, y in bomb_positions:
    #         board[x][y]["state"] = TileState.HIDDEN_MINE.name
        
        
    #     request.session["board"] = board
    # else:
    #     board = request.session["board"]

    return render(request, 'minesweeper/base.html', {"board": board, "board_y": board_y})


def open_cell(request):
    x = int(request.POST["x"])
    y = int(request.POST["y"])

    board = request.session["board"]

    # Simulate update logic (e.g., flood fill)
    to_update = [(x, y)]

    # Update board state
    for i, j in to_update:
        board[j][i]["state"] = "FLAGGED_EMPTY"

    # Render main clicked cell
    clicked_cell_html = render_to_string("partials/cell.html", {
        "cell": board[y][x],
        "x": x,
        "y": y,
        "oob": False
    })

    request.session["board"] = board
    # time.sleep(0.1)
    return HttpResponse(clicked_cell_html)
    # return HttpResponse(clicked_cell_html + oob_cells)
    
# def cell_action(request):
#     x = int(request.POST["x"])
#     y = int(request.POST["y"])
#     button = request.POST["button"]
#     print(f"Button pressed: {button}")
#     print(f"x value: {x}, y value: {y}")
    
#     # board = request.session["board"]

#     # Simulate update logic (e.g., flood fill)
#     to_update = [(x, y)]

#     if button == "0":
#         # Update board state
#         for i, j in to_update:
#             if board[j][i]["state"] == "HIDDEN_EMPTY":
#                 print("Opening empty cell")
#                 board[j][i]["state"] = "OPEN_EMPTY"
#             elif board[j][i]["state"] == "HIDDEN_MINE":
#                 print("Opening mine cell")
#                 board[j][i]["state"] = "EXPLODED_MINE"
            
#     elif button == "2":
#         if board[y][x]["state"] == "HIDDEN_EMPTY":
#             print("Flagging empty cell")
#             board[y][x]["state"] = "FLAGGED_EMPTY"
#         elif board[y][x]["state"] == "HIDDEN_MINE":
#             print("Flagging mine cell")
#             board[y][x]["state"] = "FLAGGED_MINE"
#         elif board[y][x]["state"] == "FLAGGED_EMPTY":
#             print("Unflagging empty cell")
#             board[y][x]["state"] = "HIDDEN_EMPTY"
#         elif board[y][x]["state"] == "FLAGGED_MINE":
#             print("Unflagging mine cell")
#             board[y][x]["state"] = "HIDDEN_MINE"
    

#     # Render main clicked cell
#     clicked_cell_html = render_to_string("partials/cell.html", {
#         "cell": board[y][x],
#         "x": x,
#         "y": y,
#         "oob": False
#     })
    
    
    
#     # oob_cells = render_to_string("partials/cell.html", {
#     #     "cell": board[1][1],
#     #     "x": 1,
#     #     "y": 1,
#     #     "oob": True
#     # })

#     # request.session["board"] = board
#     # time.sleep(0.2)
#     return HttpResponse(clicked_cell_html)
#     # return HttpResponse(clicked_cell_html + oob_cells)

def cell_action(request):
    x = int(request.POST["x"])
    y = int(request.POST["y"])
    button = request.POST["button"]
    print(f"Button pressed: {button}")
    print(f"x value: {x}, y value: {y}")

    # Update global board state
    to_update = [(x, y)]

    if button == "0":
        for i, j in to_update:
            if board[j][i]["state"] == "HIDDEN_EMPTY":
                print("Opening empty cell")
                board[j][i]["state"] = "OPEN_EMPTY"
            elif board[j][i]["state"] == "HIDDEN_MINE":
                print("Opening mine cell")
                board[j][i]["state"] = "EXPLODED_MINE"

    elif button == "2":
        if board[y][x]["state"] == "HIDDEN_EMPTY":
            print("Flagging empty cell")
            board[y][x]["state"] = "FLAGGED_EMPTY"
        elif board[y][x]["state"] == "HIDDEN_MINE":
            print("Flagging mine cell")
            board[y][x]["state"] = "FLAGGED_MINE"
        elif board[y][x]["state"] == "FLAGGED_EMPTY":
            print("Unflagging empty cell")
            board[y][x]["state"] = "HIDDEN_EMPTY"
        elif board[y][x]["state"] == "FLAGGED_MINE":
            print("Unflagging mine cell")
            board[y][x]["state"] = "HIDDEN_MINE"

    print("state:", board[y][x]["state"])
    # Render updated cell HTML
    updated_cell_html = render_to_string("partials/cell_content.html", {        
        "cellstate": board[y][x]["state"],
        "y": y,
        "x": x,
    })

    # Broadcast the update to all clients
    from threading import Lock
    with clients_lock:
        for q in clients:
            q.put((x, y, updated_cell_html))

    # return HttpResponse(updated_cell_html)
    return HttpResponse(status=204)


def reset(request):

    for y in range(board_y):
        for x in range(board_x):
            board[y][x] = {
                "state": TileState.HIDDEN_EMPTY.name,
                "hovered_by": None,
                "highlight": False
            }
        
    all_positions = [(x, y) for x in range(board_x) for y in range(board_y)]
    bomb_positions = random.sample(all_positions, board_mines)
    
    for x, y in bomb_positions:
        board[y][x]["state"] = TileState.HIDDEN_MINE.name
    
    # request.session["board"] = board

    return render(request, 'partials/board.html', {"board": board, "board_y": board_y})


def stream(request):
    def event_stream():
        q = queue.Queue()
        with clients_lock:
            clients.append(q)

        try:
            while True:
                x, y, html = q.get()  # wait for new updates
                yield f"event: cell-{x}-{y}\ndata: {html}\n\n"
        except GeneratorExit:
            with clients_lock:
                clients.remove(q)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

# def stream(request):
#     # time.sleep(55555)
#     print("stream")
#     def event_stream():
        
#         print("stream")
#         q = queue.Queue()
#         with clients_lock:
#             clients.append(q)

#         try:
#             while True:
#                 html = q.get()  # Block until new data is available
#                 yield f"data: {html}\n\n"
#         except GeneratorExit:
#             with clients_lock:
#                 clients.remove(q)
    
#     # def event_stream():
#     #     while True:
#     #         x = random.randint(0, board_x - 1)
#     #         y = random.randint(0, board_y - 1)
#     #         to_update = [(x, y)]

#     #         # Update board state
#     #         for i, j in to_update:
#     #             if board[j][i]["state"] == "HIDDEN_EMPTY":
#     #                 print(f"Opening empty cell at ({i}, {j})")
#     #                 board[j][i]["state"] = "OPEN_EMPTY"
#     #             elif board[j][i]["state"] == "HIDDEN_MINE":
#     #                 print(f"Opening mine cell at ({i}, {j})")
#     #                 board[j][i]["state"] = "EXPLODED_MINE"

#     #         # Render updated cell
#     #         html = render_to_string("partials/cell.html", {
#     #             "cell": board[y][x],
#     #             "x": x,
#     #             "y": y,
#     #             "oob": True
#     #         })

#     #         yield f"event: cell-{x}-{y}\ndata: {html}\n\n"
#     #         time.sleep(5)  # Simulate delay between events

#     return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
