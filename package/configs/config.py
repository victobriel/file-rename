import os,configparser as cp

class Config:
    def __init__(self, file: str = "config.ini", language: str = "en_US"):
        self.CONFIG: cp.ConfigParser = cp.ConfigParser()
        self.file = file
        if not os.path.exists(self.file):
            self.CONFIG.add_section("config")
            self.CONFIG.set("config", "backup", "False")
            self.CONFIG.set("config", "language", language)
            supported_languages = [f for f in os.listdir("package/lang/bases") if os.path.isfile(os.path.join("package/languages/bases", f)) and f.endswith(".json")]
            self.CONFIG.set('config', '# Supported languages:', ''.join(supported_languages).replace(".json", ", ").rstrip(", "))
            self.CONFIG.set('config', '# How to add new languages', 'https://github.com/victobriel/file-rename/README.md#how-add-new-language')
            self.CONFIG.set("config", "encoding", "utf-8")
            self.CONFIG.add_section("paths")
            self.CONFIG.set("paths", "protect_paths", "True")
            if os.name == "nt":
                self.CONFIG.set("paths", "protected", "C:/Windows,C:/Program Files,C:/ProgramData,AppData,System Volume Information")
            elif os.name == "posix":
                self.CONFIG.set("paths", "protected", "/etc,/bin,/usr,/var,/lib,/sbin,/dev,/proc,/boot,/sys,/run,/snap,/lib64,/lib32,/media,/mnt,/opt,/srv,/tmp,/root,/home,/lost+found,/cdrom,/usr/local,/usr/share,/usr/bin,/usr/sbin,/usr/lib,/usr/lib64,/usr/lib32,/usr/local/bin,/usr/local/sbin,/usr/local/lib,/usr/local/lib64,/usr/local/lib32,/usr/share/bin,/usr/share/sbin,/usr/share/lib,/usr/share/lib64,/usr/share/lib32,/usr/bin,/usr/sbin,/usr/lib,/usr/lib64,/usr/lib32,/bin,/sbin,/lib,/lib64,/lib32,/media,/mnt,/opt,/srv,/tmp,/root,/home,/lost+found,/cdrom,/usr/local,/usr/share,/usr/bin,/usr/sbin,/usr/lib,/usr/lib64,/usr/lib32,/usr/local/bin,/usr/local/sbin,/usr/local/lib,/usr/local/lib64,/usr/local/lib32,/usr/share/bin,/usr/share/sbin,/usr/share/lib,/usr/share/lib64,/usr/share/lib32")
            else:
                self.CONFIG.set("paths", "protected", "")

            with open(self.file, "w") as configfile:
                self.CONFIG.write(configfile)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {', '.join([f'{key}={value}' for key, value in self.__dict__.items()])}"

    def resetconfig(self) -> None:
        if os.path.exists(self.file): os.remove(self.file)
        self.__init__() #type: ignore
        
    def get(self, section, key) -> str:
        return self.CONFIG[section][key]
    
    def set(self, section, key, value) -> None:
        self.CONFIG[section][key] = value
        try:
            with open(self.file, "w") as configfile:
                self.CONFIG.write(configfile)
        except:
            self.resetconfig()

    def read(self) -> None:
        self.CONFIG.read(self.file)
