import cv2
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as tkFileDialog
import numpy as np
import os
from PIL import Image, ImageTk
import flet as ft



# Create a tkinter window



        
allInputs = []

T = []
imageDispaly='./none.png'
def main(page: ft.Page):



    page.window_width=1120
    page.window_height=705
    page.title = "Healthy Or Unhealthy ???"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Regular.ttf",


    }
    page.theme = ft.Theme(font_family="Kanit")

  
    weights = np.array([])
    image = None
    text = "_______"
    

    # <<<< upload image when  click button upload image
    async def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        
        # print("Selected files:", e.files[0].path)
        path=e.files[0].path
        imageDispaly=path
        imgInput.src=f"{imageDispaly}"
        await imgInput.update_async()
        if path:
            img = cv2.imread(path,cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(img, (300, 300), interpolation = cv2.INTER_AREA)
            cv2.imwrite(f"images/test.jpg", resized)
            im = Image.open(f"images/test.jpg")
            print(im)
            
            await neural(path)
            page.update()

        


    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)
    
    # end code upload image when  click button upload image>>>



    def isError(e):
        for i in range(len(e)):
            if(e[i][0] != 0):
                return True
        return False

    def orthonormal(pp):
        for i in range(len(pp)):
            for j in range(len(pp[0])):
                if (i==j and pp[i][j] != 1) or (i != j and pp[i][j]!=0):
                    return False
                
        return True

    def training():
        global weights, T, allInputs
        S = 1
        folder_dir = "images/Healthy/"
        for image in os.listdir(folder_dir):
            allInputs.append(flatten(cv2.imread(f"{folder_dir}/{image}",cv2.IMREAD_GRAYSCALE)) )
            T.append([1 for _ in range(S)])
        folder_dir = "images/Diseased/"
        for image in os.listdir(folder_dir):
            allInputs.append(flatten(cv2.imread(f"{folder_dir}/{image}",cv2.IMREAD_GRAYSCALE)) )
            T.append([-1 for _ in range(S)])
        allInputs = np.array(allInputs)
        T = np.array(T).transpose()

        numP =  len(allInputs)
        R = len(allInputs[0])
        
        if orthonormal(np.dot(allInputs, allInputs.transpose())):
            weights = np.dot(T, allInputs)
        else:
            weights = np.dot(T, np.dot(np.linalg.inv(np.dot(allInputs, allInputs.transpose())),allInputs))

            
        

    def flatten(image):
        new_image = []
        for row in image:
            for el in row:
                new_image.append(-1 if el<128 else 1)
        return new_image


    async def neural(path):
        global weights,text
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)  # Resize to 256x256
        p = np.array(flatten(resized))
        p = p.transpose()
        #print(p.shape, weights.shape)
        a = np.dot(weights, p)
        t.value = f" Healthy" if a[0] >= 0 else f" Diseased"
        await t.update_async()
        # text.update()
        # label2.config(text=text)
        # label2.text = text      
    t = ft.Text(text, size=26, color=ft.colors.RED, weight=ft.FontWeight.BOLD)
    imgInput=ft.Image(src=imageDispaly)
    def route_change(route):

        page.views.clear()
        page.views.append(
            ft.View(
                bgcolor="#C9E6D1",
                route="/",
                controls=[
                

                    ft.Column([
                        ft.Container(height=5),
                        ft.Row([ft.Container(width=23), ft.Image("img\Logo.png"), ft.Container(width=7),
                                ft.Image("img\plant disease detection.png")]),

                        ft.Row(
                            [
                                ft.Container(content=ft.Container(

                                    content=ft.Column([
                                      
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.icons.UPLOAD_OUTLINED, color=ft.colors.BLACK),
                                                ft.Text("Upload Image", color=ft.colors.BLACK,
                                                        style=ft.TextStyle(weight=ft.FontWeight.W_700))
                                            ]
                                                , alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            margin=ft.margin.only(top=35, left=10, right=10, bottom=2),

                                            padding=10,
                                            alignment=ft.alignment.center,
                                            bgcolor='#C9E6D1',
                                            width=177,
                                            height=42,
                                            border_radius=5,
                                            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
                                        ),
                                        selected_files,

                                        # ft.Container(content=ft.Text("Upload photo of your planet", color="#464646")
                                        #              ,
                                        #              margin=ft.margin.only(left=10, right=10),
                                        #              ),
                                        
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.icons.PREVIEW, color=ft.colors.BLACK),
                                                ft.Text("Training", color=ft.colors.BLACK,
                                                        style=ft.TextStyle(weight=ft.FontWeight.W_700))
                                            ]
                                                , alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            margin=ft.margin.only(top=10, left=15, right=10, bottom=10),
                                            padding=10,
                                            alignment=ft.alignment.center,
                                            bgcolor='#C9E6D1',
                                            width=177,
                                            height=42,
                                            border_radius=5,
                                            on_click=lambda e: training(),
                                        ),
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.icons.CLOSE, color=ft.colors.BLACK),
                                                ft.Text("Clear All", color=ft.colors.BLACK,
                                                        style=ft.TextStyle(weight=ft.FontWeight.W_700))
                                            ]
                                                , alignment=ft.MainAxisAlignment.CENTER),
                                            margin=ft.margin.only(top=30, left=10, right=10, bottom=10),
                                            padding=10,
                                            alignment=ft.alignment.center,
                                            bgcolor='#C9E6D1',
                                            width=177,
                                            height=42,
                                            border_radius=5,
                                            on_click=lambda e: print("clear all"),
                                        ),
                                        
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.BLACK),
                                                ft.Text("Exit", color=ft.colors.BLACK,
                                                        style=ft.TextStyle(weight=ft.FontWeight.W_700))
                                            ]
                                                , alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            margin=ft.margin.only(top=30, left=10, right=10, bottom=10),

                                            padding=10,
                                            alignment=ft.alignment.center,
                                            bgcolor='#C9E6D1',
                                            width=177,
                                            height=42,
                                            border_radius=5,
                                            on_click=lambda _: print("Exiting"),
                                        ),
                                        
                                    ]
                                        ,
                                    ),
                                    margin=ft.margin.only(top=10, left=20, right=10, bottom=10),
                                    padding=ft.padding.only(top=10, left=20, right=20, bottom=10),
                                    alignment=ft.alignment.center,
                                    bgcolor="#88CDA8",
                                    width=256,
                                    height=415,
                                    border_radius=24,
                                ), height=500, ),
                                ft.Container(
                                    margin=ft.margin.only(top=40, left=30),
                                    width=405,
                                      #alignment=ft.alignment.center,
                                    # bgcolor=ft.colors.RED,
                                    height=480,
                                    content=ft.Column(
                                        [
                                            ft.Row([ft.Column([ft.Container(
                                                border=ft.border.all(width=1.2, color=ft.colors.BLACK),
                                                content=imgInput, width=181, height=178),
                                                               ft.Container(
                                                                   ft.Text("input image", weight=ft.FontWeight.W_700),
                                                                   width=181, alignment=ft.alignment.center),
                                                               ft.Container(height=20), ]),
                                                    ft.Container(width=20)
                                                       , ft.Column([ft.Container(
                                                    border=ft.border.all(width=1.2, color=ft.colors.BLACK),
                                                    content=ft.Image("none.png"), width=181, height=178),
                                                                    ft.Container(ft.Text("Gary conversion",
                                                                                         weight=ft.FontWeight.W_700),
                                                                                 width=181,
                                                                                 alignment=ft.alignment.center),
                                                                    ft.Container(height=20), ]), ]),
                                            ft.Row([ft.Column([ft.Container(
                                                border=ft.border.all(width=1.2, color=ft.colors.BLACK),
                                                content=  ft.Image("none.png"), width=181, height=178),
                                                               ft.Container(
                                                                   ft.Text("Enhancement", weight=ft.FontWeight.W_700),
                                                                   width=181, alignment=ft.alignment.center),
                                                               ft.Container(height=10), ]),
                                                    ft.Container(width=20)
                                                       , ft.Column([ft.Container(
                                                    border=ft.border.all(width=1.2, color=ft.colors.BLACK),
                                                    content=  ft.Image("none.png"), width=181, height=178),
                                                                    ft.Container(ft.Text("segmentation",
                                                                                         weight=ft.FontWeight.W_700),
                                                                                 width=181,
                                                                                 alignment=ft.alignment.center),
                                                                    ft.Container(height=10), ])])

                                        ,
                                            ft.Row([
                                                ft.Text("Healthy Or Diseased ? :", size=23, weight=ft.FontWeight.BOLD)
                                                ,
                                                t,
                                          

                                            ]
                                                , alignment=ft.MainAxisAlignment.CENTER)
                                        ]
                                    )
                                    ,

                                ),

                                ft.Container(

                                    width=230,
                                    alignment=ft.alignment.center,
                                    height=428,
                                   #bgcolor=ft.colors.RED,
                                    margin=ft.margin.only(bottom=30),

                                    content=ft.Column([
                                        ft.Text("Parameters", style=ft.TextStyle(size=23, weight=ft.FontWeight.BOLD)),
                                        ft.Container(

                                            content=ft.Text("Affected Area:\n         74%",
                                                            style=ft.TextStyle(size=14, weight=ft.FontWeight.W_800))
                                            , bgcolor="#33D45F"
                                            , padding=10
                                            , width=120, height=59
                                            , margin=ft.margin.only(top=10, bottom=8)
                                        )
                                        , ft.Container(

                                            content=ft.Text("    Accurancy:\n         97%",
                                                            style=ft.TextStyle(size=14, weight=ft.FontWeight.W_800))
                                            , bgcolor="#33D45F"
                                            , width=120, height=59
                                            , padding=10
                                            , margin=ft.margin.only(top=8, bottom=8)
                                        ),
                                        ft.Container(

                                            content=ft.Text("      Mean:\n      0.15678",
                                                            style=ft.TextStyle(size=14, weight=ft.FontWeight.W_800))
                                            , bgcolor="#33D45F"
                                            , padding=10
                                            , width=120, height=59
                                            , margin=ft.margin.only(top=8, bottom=8)
                                        ),
                                        ft.Container(

                                            content=ft.Text("      Entropy:\n       5,7500",
                                                            style=ft.TextStyle(size=14, weight=ft.FontWeight.W_800))
                                            , bgcolor="#33D45F"
                                            , padding=10
                                            , width=120, height=59
                                            , margin=ft.margin.only(top=8, bottom=8)
                                        ),
                                        ft.Container(
                                            margin=ft.margin.only(top=28),

                                            content=ft.Text(
                                                color="#9F3939",
                                                style=ft.TextStyle(size=20, weight=ft.FontWeight.W_700),
                                                spans=[ft.TextSpan(
                                                    "Show Diagram",
                                                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                                                    on_click=lambda e: page.go("/showDigrame"), )]
                                            )
                                        )
                                    ]
                                        ,
                                        alignment=ft.MainAxisAlignment.CENTER))

                            ],
                            alignment=ft.MainAxisAlignment.CENTER,

                        ),

                    ]

                    )
                ],
            )
        )
        if page.route == "/showDigrame":
            page.views.append(
                ft.View(
                    "/showDigrame",
                    [
                        ft.Row([ft.Container(width=23), ft.Image("img\Logo.png"), ft.Container(width=7),
                                ft.Image("img\plant disease detection.png")]),

                        ft.Container(height=30),
                       ft.Container(
                           width=1000,
                           alignment=ft.alignment.center,
                           padding=ft.padding.only(left=380),
                           content=ft.Column([
                           ft.Container(

                               content=ft.Image("img\showDiagram.png"), width=464),
                           ft.Container(height=50),
                           ft.Row([
                               ft.Container(width=40),
                               ft.ElevatedButton("Back to Result", color=ft.colors.BLACK, bgcolor="#33D45F",
                                                 on_click=lambda _: page.go("/")),
                              ft.Container(width=40),
                               ft.ElevatedButton("Download Diagram", color=ft.colors.BLACK, bgcolor="#33D45F",
                                                 on_click=lambda _: print("Downloads"))]),
                       ])
                       )

                    ],
                    bgcolor="#C9E6D1",
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


print(imageDispaly)
ft.app(target=main )










