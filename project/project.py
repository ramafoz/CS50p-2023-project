import csv
from datetime import datetime
import math
import pandas as pd
import numpy as np
import sys
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def main():
    size = get_size()
    max_pop = size*size
    gen = get_generations()
    run = get_runs()
    if args.g>=1:
            clean_slate(size)
    for j in range(run):
        v_print(f"Running simulation number {j+1}")
        vv_print(f"Running simulation number {j+1}")
        field = get_matrix(size)
        pop = get_pop(field)
        if args.g>=1:
            show_field(field, gen, None, run, j, pop, max_pop, None)
        v_print(f"Starting 'field':\n{field}\n"\
                +f"(Start population = {pop}, {(pop/max_pop):07.2%})\n")
        vv_print(f"Starting 'field':\n{field}\n"\
                 +f"(Start population = {pop}, {(pop/max_pop):07.2%})\n")

        if (args.r>=1):
            write_log(None, None, j, run, pop, max_pop, size, None, gen)

        if (args.i>=1):
            confirm = input(f"Run Game {j+1:04d}/{run:04d}? (y/n): ").upper()
            if confirm == "":
                confirm = "Y"
            elif confirm != "Y":
                sys.exit("Conway's Game of Life Aborted")

        fields = list()
        fields.append(field)
        pops = list()
        pops.append(pop)

        for _ in range(gen):
            if (args.i>=2):
                confirm = input(f"Run Gen {_+1:04d}/{gen:04d}? (y/n): ").upper()
                if confirm == "":
                    confirm = "Y"
                elif confirm != "Y":
                    sys.exit("Conway's Game of Life Aborted")

            vv_print(f"Run {j+1:04d}/{run:04d} --> Gen {_+1:05d}/{gen:05d}")
            new_field = conway(field)
            fields.append(new_field)
            new_pop = get_pop(new_field)
            pops.append(new_pop)
            show_field(new_field, gen, _, run, j, pop, max_pop, new_pop)

            if args.r>=1:
                write_log(None, None, j, run, pop, max_pop, size, _, gen)


            vv_print(new_field)
            if args.v > 1:
                print(f"(Population: = {new_pop}, {(new_pop/max_pop):07.2%})\n")

            if check_changes(field, new_field) == "Go on":
                if check_loops(new_field, fields) == "Go on":
                    field = new_field
                    pop = new_pop
                else:
                    result = ("Loop starts at generation "+
                        f"{check_loops(new_field, fields)-1}"
                        "\nand first repeats",
                        _+1)
                    break
            else:
                result = (check_changes(field, new_field), _+1)
                break
            if _ == (gen-1):
                result = ("Life, uh, finds a way.\nStill evolving", gen)

        vresult,iresult = result
        printres = (f"Run {j+1:04d}/{run:04d}:\n"\
                    +f"{vresult} at generation {iresult}.\n"\
                    +f"(Final population = {new_pop}, {(new_pop/max_pop):07.2%})\n")
        print (printres)
        v_print ("")
        vv_print("")
        if (args.g>=1):
            show_result(field, printres, iresult, j, run)
            create_gif(j, size)

        if (args.r>=1):
            write_log(printres, iresult, j, run, new_pop, max_pop, size, None, gen)

    if (args.g>=1):
        clean_folder()


def get_size():
    try:
        n = args.n
        if (n <= 1) or (n > 480):
            raise ValueError
        else:
            return n
    except ValueError:
        sys.exit("Invalid input")

def get_generations():
    try:
        n = args.t
        if (n <= 0) or(n > 10000) :
            raise ValueError
        else:
            return n
    except ValueError:
        sys.exit("Invalid input")

def get_runs():
    try:
        n = args.s
        if (n <= 0) or(n > 1000) :
            raise ValueError
        else:
            return n
    except ValueError:
        sys.exit("Invalid input")

def get_pop(f):
    return np.sum(f)

def get_matrix(n):
#   Generates random n x n matrix with values 0 or 1
    m = np.random.randint(0, 2, size=(n,n))
#   For a True/False n x n matrix
#   m = (m == 1)
    return (m)

def clean_slate(n):
    for file in os.listdir(f"{folder}"):
        if file.startswith(f"_gif_cgl{n:03d}"):
            os.remove(f"{folder}/{file}")

def show_field(m, gen, _, run, k, pop, max_pop, new_pop):
    if (args.g>=1):
        im_size = 2048
        n = len(m)
        cell_size = int(round(im_size/n))
        im_size = cell_size * n
        im = Image.new("1", (im_size, im_size))
        for i in range (n):
            for j in range (n):
                if m[i][j] == 1:
                    color = 0
                else:
                    color = 255
                im.paste(
                    color,
                    (cell_size*j, cell_size*i, cell_size*(j+1), cell_size*(i+1))
                    )
        color = 255
        label = Image.new("1", (im_size,int(im_size/16)), 255)
        fontsize = 10
        fnt = ImageFont.truetype("arial.ttf",fontsize)
        fillertxt = (" Size 999 CGL" +
            " -> Run 9999/9999" +
            " -> Gen 99999/99999"+
            " -> Pop: 999999, 999.99%}")
        if _ is None:
            txt1 = (f" Size {n:03d} CGL -> Run {k+1:04d}/{run:04d} -> "+
            f"Starting Pop: {pop:06d}, {(pop/max_pop):07.2%}")
        else:
            txt2 = (f" Size {n:03d} CGL" +
            f" -> Run {k+1:04d}/{run:04d}" +
            f" -> Gen {_+1:05d}/{gen:05d}"+
            f" -> Pop: {new_pop:06d}, {(new_pop/max_pop):07.2%}")
        breakpoint = 3 * im_size /4
        jumpsize = 5
        while True:
            if fnt.getbbox(fillertxt)[2] < breakpoint:
                fontsize += jumpsize
            else:
                jumpsize = jumpsize // 2
                fontsize -= jumpsize
            fnt = ImageFont.truetype("arial.ttf", fontsize)
            if jumpsize <= 1:
                break
        draw = ImageDraw.Draw(label)
        if _ is None:
            draw.text((10,10), txt1, font=fnt, fill=0)
        else:
            draw.text((10,10), txt2, font=fnt, fill=0)
        f_image = Image.new("1",(im_size,int(im_size+im_size/16)))
        f_image.paste(im, (0,0))
        f_image.paste(label, (0,im_size))
        if (args.g>=1):
            if _ is None:
                filename = f"{folder}/temp/cgl_n{n:03d}_r{k+1:04d}_g{0:05d}.png"
            else:
                filename = f"{folder}/temp/cgl_n{n:03d}_r{k+1:04d}_g{_+1:05d}.png"
            f_image.save(filename)

def show_result(m, printres, iresult, k, run):
    im_size = 2048
    n = len(m)
    cell_size = int(round(im_size/n))
    im_size = cell_size * n
    f_image = Image.new("1", (im_size, int(im_size+im_size/16)), 255)
    fillertxt = (" Size 999 CGL" +
            " -> Run 9999/9999" +
            " -> Gen 99999/99999"+
            " -> Pop: 999999, 999.99%}")
    fontsize = 10
    fnt = ImageFont.truetype("arial.ttf", fontsize)
    breakpoint = 3 * im_size /4
    jumpsize = 5
    while True:
            if fnt.getbbox(fillertxt)[2] < breakpoint:
                fontsize += jumpsize
            else:
                jumpsize = jumpsize // 2
                fontsize -= jumpsize
            fnt = ImageFont.truetype("arial.ttf", fontsize)
            if jumpsize <= 1:
                break

    draw = ImageDraw.Draw(f_image)
    draw.text(
        (25,im_size/2),
        f"{printres}",
        font=fnt,
        fill=0,
        )
    draw.text(
        (10,im_size+10),
        f" Size {n:03d} CGL --> Run {k+1:04d}/{run:04d} --> End",
        font=fnt,
        fill=0
        )
    filename = f"{folder}/temp/cgl_n{n:03d}_r{k+1:04d}_g{iresult+1:05d}_end.png"
    f_image.save(filename)


def create_gif(run, n):

    im_size = 2048
    cell_size = int(round(im_size/n))
    im_size = cell_size * n
    gif_image = Image.new('1', (im_size,int(im_size+im_size/16)), 255)

    if not os.path.exists(f"{folder}/temp"):
        os.makedirs(f"{folder}/temp")

    images = []
    for file in os.listdir(f"{folder}/temp"):
        if file.startswith(f"cgl_n{n:03d}_r{run+1:04d}"):
            images.append(Image.open(f"{folder}/temp/{file}"))

    filename = f"{folder}/_gif_cgl{n:03d}_run{run+1:04d}.gif"

    if 0 < len(images) <= 900:
        pictime = 200
    elif 900 < len(images):
        pictime = 180000/len(images)

    gif_image.save(filename,
        format="GIF",
        save_all=True,
        append_images=images[0:],
        duration=pictime,
        )

def write_log(printres, iresult, j, run, new_pop, max_pop, size, i, gen):
    with open(log_filename, 'a', newline='') as f:
        fwrite = csv.writer(f)
        timestamp = datetime.now()
        if (printres is None) and (i is not None):
            log_entry = [timestamp, f"{size:03d}", f"{j+1:05d}/{run:05d}",
                        "Running", f"{i+1:05d}/{gen:05d}",
                        f"{new_pop:06d}", f"{(new_pop/max_pop):07.2%}"]
        elif (printres is None):
            log_entry = [timestamp, f"{size:03d}", f"{j+1:05d}/{run:05d}",
                        "Starting", f"00000/{gen:05d}",
                        f"{new_pop:06d}", f"{(new_pop/max_pop):07.2%}"]
        else:
            if "uh" in printres:
                resu = "EVOLVING"
            elif "Loop" in printres:
                resu = "LOOP"
            elif "Dead" in printres:
                resu = "EMPTY"
            elif "Stag" in printres:
                resu = "FROZEN"

            log_entry = [timestamp, f"{size:03d}", f"{j+1:05d}/{run:05d}",
                         "End of run", f"{iresult:05d}/{iresult:05d}",
                         f"{new_pop:06d}", f"{(new_pop/max_pop):07.2%}",
                         resu]
        fwrite.writerow(log_entry)
        f.close()


def clean_folder():
    for file in os.listdir(f"{folder}/temp"):
       os.remove(f"{folder}/temp/{file}")
    os.rmdir(f"{folder}/temp")


def plot():
    df = pd.read_csv(
        f"{data_filename}",
        names=["timestamp","size", "run", "status", "gen", "pop", "percent", "end"],
        dtype={"timestamp":str, "size":int, "run":str,
        "status":str, "gen":str, "pop":int, "percent":str, "end":str})
    size_list = []
    size_list = df["size"].tolist()
    size_list.sort()
    size_list_compressed = []
    for i in size_list:
        if i in size_list_compressed:
            pass
        else:
            size_list_compressed.append(i)
    size_list = size_list_compressed
    while True:
        plot_type = input("\nEnter Plot type: \n"
                          +"1. Evolution of total population \n"
                          +"2. Comparison of population % \n"
                          +"3. Length of runs by size \n"
                          +"4. End results by size \n"
                          +"Enter Plot type number: ")
        if plot_type not in ["1", "2", "3", "4"]:
            print("Invalid Input")

        elif plot_type == "1":
            try:
                data_size = int(input(f"Choose matrix size: \n {size_list}\n"))
                if data_size not in size_list:
                    print("Invalid Input")
            except ValueError:
                print("Invalid Input")
            else:
                break

        elif plot_type == "2":
            valid_input = False
            while not valid_input:
                len_sizes = input("Choose how many sizes to compare [up to 4]:")
                if len_sizes not in ["2","3","4"]:
                    print("Invalid input")
                else:
                    len_sizes = int(len_sizes)
                    valid_input = True
            data_sizes = []
            i = 0
            while i < len_sizes:
                try:
                    d_size = int(input(f"Choose matrix size: \n {size_list}\n"))
                    if d_size not in size_list:
                        raise ValueError("Invalid Input")
                    elif d_size in data_sizes:
                        raise ValueError("Duplicated Value")
                    else:
                        data_sizes.append(d_size)
                        i += 1
                except ValueError:
                    print("Invalid Input")
            data_sizes.sort()
            break

        elif plot_type == "3":
            valid_input = False
            while not valid_input:
                len_sizes = input("Choose how many sizes to plot [up to 4]:")
                if len_sizes not in ["1","2","3","4"]:
                    print("Invalid input")
                else:
                    len_sizes = int(len_sizes)
                    valid_input = True
            data_sizes = []
            i = 0
            while i < len_sizes:
                try:
                    d_size = int(input(f"Choose matrix size: \n {size_list}\n"))
                    if d_size not in size_list:
                        raise ValueError("Invalid Input")
                    elif d_size in data_sizes:
                        raise ValueError("Duplicated Value")
                    else:
                        data_sizes.append(d_size)
                        i += 1
                except ValueError:
                    print("Invalid Input")
            data_sizes.sort()
            break

        elif plot_type == "4":
            valid_input = False
            while not valid_input:
                len_sizes = input("Choose how many sizes to plot [up to 8]:")
                if len_sizes not in ["1","2","3","4","5","6","7", "8"]:
                    print("Invalid input")
                else:
                    len_sizes = int(len_sizes)
                    valid_input = True
            data_sizes = []
            i = 0
            while i < len_sizes:
                try:
                    d_size = int(input(f"Choose matrix size: \n {size_list}\n"))
                    if d_size not in size_list:
                        raise ValueError("Invalid Input")
                    elif d_size in data_sizes:
                        raise ValueError("Duplicated Value")
                    else:
                        data_sizes.append(d_size)
                        i += 1
                except ValueError:
                    print("Invalid Input")
            data_sizes.sort()
            break


        else:
            break
    if plot_type == "1":
        plot1(df, data_size)
    if plot_type == "2":
        plot2(df, data_sizes)
    if plot_type == "3":
        plot3(df, data_sizes)
    if plot_type == "4":
        plot4(df, data_sizes)



def plot1(df, data_size):
    df_filtered = df.loc[df["size"] == data_size]
    for run in df_filtered["run"].unique():
        df_run = df_filtered.loc[(df_filtered["run"] == run)
                                    & (df_filtered["status"] == "Running")].copy()
        df_run.loc[:,"gen1"] = df_run["gen"].str.split("/").str[0].astype(int)
        plt.scatter(df_run["gen1"], df_run["pop"],
                    s=0.1, c = np.array([[0.2,0.8,1]]),
                    alpha=0.3)
        plt.xlabel("Generation")
        plt.ylabel("Population")
        plt.title(f"Population Graph for size {data_size} CGL's")
        plt.grid()
    df_mean = df_filtered[(df_filtered["status"] == "Running")].copy()
    df_mean.loc[:,"gen1"] = df_mean["gen"].str.split("/").str[0].astype(int)
    df_mean_pop = df_mean.groupby("gen1")["pop"].mean()
    plt.plot(df_mean_pop.index, df_mean_pop.values, c = np.array([[0,0,1]]),
             label=f"Mean pop. for Size {data_size}")

    df_fin = df_filtered[(df_filtered["status"] == "End of run")].copy()
    df_fin.loc[:,"gen1"] = df_fin["gen"].str.split("/").str[0].astype(int)
    min_gen1 = df_fin["gen1"].min()
    max_gen1 = df_fin["gen1"].max()
    min_run = df_fin.loc[(df_fin["gen1"] == min_gen1), "run"].iloc[0]
    max_run = df_fin.loc[(df_fin["gen1"] == max_gen1), "run"].iloc[0]

    df_min = df_filtered.loc[(df_filtered["run"] == min_run) &
                            (df_filtered["status"] == "Running")].copy()
    df_min.loc[:,"gen1"] = df_min["gen"].str.split("/").str[0].astype(int)
    df_max = df_filtered.loc[(df_filtered["run"] == max_run) &
                             (df_filtered["status"] == "Running")].copy()
    df_max.loc[:,"gen1"] = df_max["gen"].str.split("/").str[0].astype(int)

    plt.plot(df_min["gen1"], df_min["pop"], c = np.array([[0,0.5,1]]),
             alpha = 0.5, linewidth = 1,
             label=f"Shortest run: {min_gen1} generations")
    plt.plot(df_max["gen1"], df_max["pop"], c = np.array([[0,0,0.5]]),
             alpha = 0.5, linewidth = 1,
             label=f"Longest run: {max_gen1} generations")

    plt.legend(loc="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()



def plot2(df, data_sizes):
    colorlist =[np.array([[0.2,0.8,1]]),
                np.array([[0.8,0,0.2]]),
                np.array([[0.8,1,0.2]]),
                np.array([[0.2,0.8,0]])]
    j = 0
    for data_size in data_sizes:
        co_ = colorlist[j]
        df_fil = df.loc[df["size"] == data_size].copy()
        df_fil.loc[:,"gen1"] = df_fil["gen"].str.split("/").str[0].astype(int)
        df_fil.loc[:,"pc1"] = df_fil["percent"].str.split("%").str[0].astype(float)
        max_gen1 = df_fil["gen1"].max()
        df_fil = df_fil.assign(pcgen=df_fil["gen1"]/max_gen1)
        for run in df_fil["run"].unique():
            df_run = df_fil.loc[(df_fil["run"] == run)
                                        & (df_fil["status"] == "Running")].copy()
            plt.scatter(df_run["pcgen"], df_run["pc1"],
                        s=0.1, c = co_, alpha=0.1)
            plt.xlabel("Generation as fraction of longest run")
            plt.ylabel("Population %")
            plt.title("Population comparison for CGL's")
            plt.grid()
        df_mean = df_fil[(df_fil["status"] == "Running")].copy()
        df_mean_pop = df_mean.groupby("pcgen")["pc1"].mean()
        plt.plot(df_mean_pop.index, df_mean_pop.values,
                label=f"Mean pop. % for Size {data_size}",
                color= co_, alpha=1
                )
        plt.legend(loc="upper right")
        j += 1
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def plot3(df, data_sizes):
    colorlist =[np.array([[0.2,0.8,1]]),
            np.array([[0.8,0,0.2]]),
            np.array([[0.8,1,0.2]]),
            np.array([[0.2,0.8,0]])]
    j = 0
    fig, axes = plt.subplots(len(data_sizes), squeeze = False)
    for i, data_size in enumerate(data_sizes):
        co_ = colorlist[j]
        ai = axes.flatten()[i]
        df_filtered = df.loc[(df["size"] == data_size) &
        (df["status"] == "End of run")].copy()
        df_filtered.loc[:,"gen1"] = df_filtered["gen"].str.split("/").str[0].astype(int)
        k = 0
        for _ in df_filtered["run"].unique():
            k += 1
        min_gen1 = df_filtered["gen1"].min()
        max_gen1 = df_filtered["gen1"].max()
        if max_gen1-min_gen1 > 100:
            step = int(math.ceil((max_gen1 - min_gen1)/100))
            if step < 25:
                step=25
        elif (100 > max_gen1-min_gen1) and ( max_gen1-min_gen1 > 50):
            step = int(math.ceil((max_gen1 - min_gen1)/50))
            if step < 25:
                step=25
        else:
            step = max_gen1 - min_gen1
        ai.hist(df_filtered["gen1"],bins=step,color=co_, histtype="stepfilled",
                weights=[1/k] * len(df_filtered["gen1"]),
                alpha = 0.5,
                label=f"Lenghts of size {data_size} CGL")
        ai.set_xlim(0,max_gen1*1.1)
        ai.set_ylabel("Frequency")
        ai.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        ai.grid()
        ai.legend(loc="upper right")

        d_mean = np.mean(df_filtered["gen1"])
        d_median = np.median(df_filtered["gen1"])
        countin = np.bincount(df_filtered["gen1"])
        d_mode = np.argmax(countin)
        ai.axvline(x=d_mean, color=co_, label=f"Mode: {d_mode}")
        ai.text(x=d_mean*1.1, y=0.01, s=f"Mean: {round(d_mean, 2)}\n"
                +f"Median: {round(d_median, 2)}\n"
                +f"Mode: {round(d_mode, 2)}\n", ha="left")

        ax2 = ai.twinx()
        ax2.set_xlim(0, max_gen1*1.1)
        ax2.yaxis.set_visible(False)
        j += 1

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.grid(False)
    plt.xlabel("End generation")


    plt.suptitle("Frequency for end generation of CGL simulations")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()



def plot4(df, data_sizes):
    colorlist =[np.array([[0.2,0.8,1]]),
        np.array([[0.8,0,0.2]]),
        np.array([[0.8,1,0.2]]),
        np.array([[0.2,0.8,0]]),
        np.array([[1,1,0]]),
        np.array([[1,0,1]]),
        np.array([[0,1,1]]),
        np.array([[0.5,0.5,0.5]])
        ]
    expected_values = ["EMPTY", "FROZEN", "LOOP", "EVOLVING"]
    width_=1/len(data_sizes)
    x = np.arange(len(expected_values))
    j = 0
    for data_size in data_sizes:
        co_ = colorlist[j]
        df_fil = df.loc[(df["size"] == data_size) &
                         (df["status"] == "End of run")].copy()
        k = 0
        for _ in df_fil["run"].unique():
            k += 1

        df_e=df_fil.groupby(["end"],sort=False)["end"].size().reset_index(name="total")
        df_e["pos"] = df_e["end"].apply(lambda x: expected_values.index(x))

        for i, value in enumerate(expected_values):
            if value in df_e["end"].values:
                pass
            else:
                new_row = pd.DataFrame({"end": [value], "total": [0], "pos": [i]})
                df_e = pd.concat([df_e[df_e["pos"] < i], new_row,
                                        df_e[df_e["pos"] >= i]]).reset_index(drop=True)
        df_e = df_e.sort_values(by="pos")
        df_e.drop("pos", axis=1, inplace=True)
        df_e = df_e.assign(pc=df_e["total"]/k)

        plt.bar(x -(0.8*width_/2)*len(data_sizes) + 0.8*width_/2 + j*width_*0.8,
                df_e["pc"], color=co_,
                width=width_*0.8,
                label=f"Lenghts of size {data_size} CGL")
        plt.xlabel("End type")
        plt.ylabel("Frequency")
        plt.grid()
        plt.legend(loc="upper right")
        j += 1
    plt.xticks(range(len(expected_values)), expected_values)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.suptitle("Frequency for each end of CGL simulations")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()





def conway(m):
    n = len(m)
    new_m = m.copy()
    for i in range (n):
        for j in range (n):
            if i == 0:
                if j == 0:
                    #corner_case_top_left
                    total = m[i+1][j]+m[i+1][j+1]+m[i][j+1]
                elif j == n-1:
                    #corner_case_top_right
                    total = m[i+1][j]+m[i+1][j-1]+m[i][j-1]
                else:
                    #top_row_case
                    total = m[i+1][j-1]+m[i+1][j]+m[i+1][j+1]+m[i][j-1]+m[i][j+1]
            elif i == n-1:
                if j == 0:
                    #corner_case_bottom_left
                    total = m[i-1][j]+m[i-1][j+1]+m[i][j+1]
                elif j == n-1:
                    #corner_case_bottom_right
                    total = m[i-1][j]+m[i-1][j-1]+m[i][j-1]
                else:
                    #bottom_row_case
                    total = m[i-1][j-1]+m[i-1][j]+m[i-1][j+1]+m[i][j-1]+m[i][j+1]
            else:
                if j == 0:
                    #left_column_case
                    total = m[i-1][j]+m[i+1][j]+m[i-1][j+1]+m[i][j+1]+m[i+1][j+1]
                elif j == n-1:
                    #right_column_case
                    total = m[i-1][j]+m[i+1][j]+m[i-1][j-1]+m[i][j-1]+m[i+1][j-1]
                else:
                    #typical case
                    total = (m[i-1][j-1]+m[i-1][j]+m[i-1][j+1]
                    + m[i][j-1]+m[i][j+1]
                    + m[i+1][j-1]+m[i+1][j]+m[i+1][j+1])

            if total == 3:
                 new_m[i][j] = 1
            elif m[i][j] == 1 and (total < 2 or total > 3):
                 new_m[i][j] = 0

    return new_m


def check_changes(m,n):
        if np.all(n == 0):
            return ("Dead field")
        elif np.all(n == m):
            return ("Stagnation")
        else:
            return ("Go on")

def check_loops(n,mlist):
        i = 0
        for m in mlist[0:len(mlist)-1]:
            i = i+1
            if np.all(n == m):
                return i
            else:
                continue
        return ("Go on")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=("This program runs 's' simulations of Conway's Game of Life (CGL) of \
                    size 'n' [n x n] for 'g' generations.")
        )
    parser.add_argument("-n", default=25, help="Size of the 'field'. Default = 25. \
                        Must be an integer between 2 and 480.", type=int)
    parser.add_argument("-t", default=250, help="Maximum number of 'generations' for each \
                        simulation. Each run will stop when 'field' loops or stagnates.\
                        Default = 250. Must be an integer between 1 and 10000", type=int)
    parser.add_argument("-s", default=25, help="Total number of games run. Default = 25. \
                        Must be an integer between 1 and 1000", type=int)
    parser.add_argument("-v", action="count", default=0, help="Verbose mode, \
                        -v prints initial stage and which 'simulation' is running, \
                        -vv prints every 'field' stage")
    parser.add_argument("-i", action="count", default=0, help="Interactive mode, \
                        prompts the user for each new run with -i, \
                        and for each new generation with -ii")
    parser.add_argument("-g", action="count", default=0, help="Graphic mode, \
                        saves a GIF for each run on a folder called 'cgl_images'. Creates \
                        the folder if needed in the same root of the Python file. If the \
                        folder exists, removes all GIF files for the same 'field' size")
    parser.add_argument("-r", action="count", default=0, help="Recording mode, \
                        writes on a csv file ('cgl_log.csv') with data for each run")
    parser.add_argument("-p", action="count", default=0, help="Plot mode, reads data on \
                        cgl_log.csv and plots the data requested by the user.")
    args = parser.parse_args()
    v_print = print if (args.v==1) or (args.i==1) else lambda *a, **k: None
    vv_print = print if (args.v>=2) or (args.i>=2) else lambda *a, **k: None

    if args.g>=1:
        folder = "cgl_images"
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(f"{folder}/temp"):
            os.makedirs(f"{folder}/temp")

    if args.r>=1:
        log_folder = "cgl_logs"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        log_filename = f"{log_folder}/cgl_log.csv"
        if not os.path.isfile(log_filename):
            df = pd.DataFrame()
            df.to_csv(log_filename)

    if args.p>=1:
        data_folder = "cgl_logs"
        if not os.path.exists(data_folder):
            sys.exit("Data not found")
        data_filename = f"{data_folder}/cgl_log.csv"
        if not os.path.isfile(data_filename):
            sys.exit("Data not found")



    if __name__ == "__main__" and args.p == 0:
        main()
    elif args.p > 0:
        plot()