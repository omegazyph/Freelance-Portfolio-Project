 try:
            self.logo_img = tk.PhotoImage(file="logo.png")
            logo_label = tk.Label(main_frame, image=self.logo_img, bg="#f0f2f5")
            logo_label.pack(pady=(0, 10))
        except Exception:
            # If no logo exists, we provide a placeholder padding
            tk.Frame(main_frame, height=10, bg="#f0f2f5").pack()
            print("Cant find logo!!!!!")