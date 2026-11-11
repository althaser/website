const html = document.documentElement;
let skillBarsInitialized = false;

const fixThemeToggleIcon = (theme) => {
  document.querySelectorAll("[data-theme-icon]").forEach((icon) => {
    icon.toggleAttribute("hidden", icon.dataset.themeIcon !== theme);
  });
};

const setTheme = (theme) => {
  const resolvedTheme = theme === "dark" ? "dark" : "light";

  html.classList.remove("light", "dark");
  html.classList.add(resolvedTheme);
  window.localStorage.setItem("theme", resolvedTheme);
  fixThemeToggleIcon(resolvedTheme);
};

const getPreferredTheme = () => {
  const storedTheme = window.localStorage.getItem("theme");

  if (storedTheme) {
    return storedTheme;
  }

  if (html.classList.contains("dark")) {
    return "dark";
  }

  if (html.classList.contains("light")) {
    return "light";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
};

const getAccordionItems = () =>
  Array.from(document.querySelectorAll("[data-accordion-item]"));

const getAccordionPanel = (item) => item?.querySelector(".panel");

const getAccordionTrigger = (item) => item?.querySelector("[data-accordion-trigger]");

const pendingPanelTransitions = new WeakMap();

const afterPanelTransition = (panel, done) => {
  panel.removeEventListener("transitionend", pendingPanelTransitions.get(panel));

  if (parseFloat(getComputedStyle(panel).transitionDuration) === 0) {
    done();
    return;
  }

  const handler = (event) => {
    if (event.target !== panel || event.propertyName !== "max-height") {
      return;
    }

    panel.removeEventListener("transitionend", handler);
    done();
  };

  pendingPanelTransitions.set(panel, handler);
  panel.addEventListener("transitionend", handler);
};

const syncAccordionItem = (item, animate = false) => {
  const panel = getAccordionPanel(item);
  const trigger = getAccordionTrigger(item);
  const isActive = item?.classList.contains("active");

  if (!panel || !trigger) {
    return;
  }

  trigger.setAttribute("aria-expanded", isActive ? "true" : "false");

  if (!isActive) {
    if (!animate || panel.hidden) {
      panel.style.maxHeight = "";
      panel.hidden = true;
      return;
    }

    panel.style.maxHeight = "0px";
    afterPanelTransition(panel, () => {
      panel.hidden = true;
      panel.style.maxHeight = "";
    });
    return;
  }

  panel.hidden = false;

  if (animate) {
    panel.style.maxHeight = "0px";
    panel.style.maxHeight = `${panel.scrollHeight}px`;
    afterPanelTransition(panel, () => {
      panel.style.maxHeight = "";
    });
  }

  initializeSkillBars(panel);
};

const syncActiveAccordionPanel = (animate = false) => {
  getAccordionItems().forEach((item) => syncAccordionItem(item, animate));
};

const initializeSkillBars = (root = document) => {
  if (skillBarsInitialized) {
    return;
  }

  const skillBars = root.querySelectorAll("[data-skill-rating]");

  if (!skillBars.length) {
    return;
  }

  skillBars.forEach((bar) => {
    bar.style.width = `${bar.dataset.skillRating}%`;
  });

  skillBarsInitialized = true;
};

const expandAccordion = (element) => {
  const item = element?.matches?.("[data-accordion-item]")
    ? element
    : element?.closest?.("[data-accordion-item]");

  if (!item) {
    return;
  }

  const items = getAccordionItems();
  const isActive = item.classList.contains("active");

  items.forEach((accordionItem) => {
    const panel = getAccordionPanel(accordionItem);

    if (panel && !panel.hidden && !panel.style.maxHeight) {
      panel.style.maxHeight = `${panel.scrollHeight}px`;
    }
  });
  void document.body.offsetHeight;

  items.forEach((accordionItem) => accordionItem.classList.remove("active"));

  if (!isActive) {
    item.classList.add("active");
  }

  syncActiveAccordionPanel(true);
};

const initializeSearch = () => {
  const searchElement = document.querySelector("#search");

  if (!searchElement || !window.PagefindUI) {
    return;
  }

  const search = new window.PagefindUI({ element: "#search", showSubResults: false, autofocus: true, pageSize: 10 });
  const query = new URLSearchParams(window.location.search).get("q");

  if (query) {
    search.triggerSearch(query);
  }

  const syncQueryToUrl = () => {
    const input = searchElement.querySelector(".pagefind-ui__search-input");
    const url = new URL(window.location.href);
    const term = input?.value.trim() ?? "";

    if (term) {
      url.searchParams.set("q", term);
    } else {
      url.searchParams.delete("q");
    }

    window.history.replaceState(null, "", url);
  };

  const getThumbLink = (event) =>
    event.target
      .closest(".pagefind-ui__result-thumb")
      ?.closest(".pagefind-ui__result")
      ?.querySelector(".pagefind-ui__result-link");

  searchElement.addEventListener("input", syncQueryToUrl);
  searchElement.addEventListener("auxclick", (event) => {
    const link = getThumbLink(event);

    if (link && event.button === 1) {
      window.open(link.href, "_blank", "noopener");
    }
  });
  searchElement.addEventListener("click", (event) => {
    const link = getThumbLink(event);

    if (link) {
      if (event.ctrlKey || event.metaKey || event.shiftKey) {
        window.open(link.href, "_blank", "noopener");
      } else {
        window.location.assign(link.href);
      }
      return;
    }

    if (event.target.closest(".pagefind-ui__search-clear")) {
      window.setTimeout(() => {
        syncQueryToUrl();
        searchElement.querySelector(".pagefind-ui__search-input")?.focus();
      });
    }
  });
};

const initializePostNavigation = () => {
  document.addEventListener("keydown", (event) => {
    const target = event.target;
    const isEditable =
      target instanceof HTMLElement &&
      (target.isContentEditable ||
        ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));

    if (isEditable) {
      return;
    }

    if (event.key === "ArrowLeft") {
      document.querySelector("[data-pager-prev]")?.click();
    }

    if (event.key === "ArrowRight") {
      document.querySelector("[data-pager-next]")?.click();
    }
  });

  if (!document.querySelector("[data-pager-prev], [data-pager-next]")) {
    return;
  }

  const scrollsHorizontally = (element) => {
    for (let node = element; node && node !== document.body; node = node.parentElement) {
      const overflowX = getComputedStyle(node).overflowX;
      if ((overflowX === "auto" || overflowX === "scroll") && node.scrollWidth > node.clientWidth) {
        return true;
      }
    }
    return false;
  };

  let swipe = null;

  document.addEventListener(
    "touchstart",
    (event) => {
      const touch = event.touches[0];
      const edge = 24;
      swipe =
        event.touches.length === 1 &&
        touch.clientX > edge &&
        touch.clientX < window.innerWidth - edge &&
        !event.target.closest("input, textarea, select, [contenteditable]") &&
        !scrollsHorizontally(event.target)
          ? { x: touch.clientX, y: touch.clientY, time: event.timeStamp }
          : null;
    },
    { passive: true },
  );

  document.addEventListener(
    "touchend",
    (event) => {
      if (!swipe || event.touches.length > 0) {
        swipe = null;
        return;
      }

      const touch = event.changedTouches[0];
      const dx = touch.clientX - swipe.x;
      const dy = touch.clientY - swipe.y;
      const elapsed = event.timeStamp - swipe.time;
      swipe = null;

      if (
        Math.abs(dx) < 80 ||
        Math.abs(dx) < Math.abs(dy) * 2 ||
        elapsed > 600 ||
        String(window.getSelection()).length > 0
      ) {
        return;
      }

      document.querySelector(dx < 0 ? "[data-pager-next]" : "[data-pager-prev]")?.click();
    },
    { passive: true },
  );

  document.addEventListener("touchcancel", () => {
    swipe = null;
  });
};

const initializeTerminal = () => {
  const screen = document.querySelector("[data-terminal-screen]");
  const source = document.querySelector("[data-terminal-script]");

  if (!screen || !source) {
    return;
  }

  const terminal = screen.closest(".terminal");
  const setBooting = (booting) => terminal?.classList.toggle("is-booting", booting);
  const resetScreen = () => screen.classList.remove("is-locked", "is-tight", "is-canvas");

  let config;
  try {
    config = JSON.parse(source.textContent);
  } catch {
    setBooting(false);
    return;
  }

  const prompt = config.prompt ?? "$ ";
  const sessions = config.sessions ?? [];

  if (!sessions.length) {
    setBooting(false);
    return;
  }

  const escapeHtml = (text) =>
    text.replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
  const markup = (text) =>
    escapeHtml(text).replace(/\{(green|blue|yellow|red|magenta|cyan|gray|debian|ubuntu|arch|freebsd|openbsd)\}(.*?)\{\/\}/g, '<span class="term-$1">$2</span>');
  const outputLines = (session) => (session.output ? session.output.replace(/\n+$/, "").split("\n") : []);
  const rainbow = (text, row) =>
    [...text]
      .map((char, col) =>
        char === " " ? char : `<span class="term-rainbow" style="--hue:${Math.round((405 - col * 1.8 - row * 3) % 360)}">${escapeHtml(char)}</span>`,
      )
      .join("");
  const outputHtml = (session, line, index) => {
    const content = session.lolcat ? rainbow(line, index) : markup(line);
    return session.tight ? `<span class="term-tight">${content || " "}</span>` : `${content}\n`;
  };
  const cursor = '<span class="terminal-cursor"></span>';

  let hiddenAt = document.hidden ? performance.now() : null;
  let hiddenTotal = 0;
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      hiddenAt = performance.now();
    } else if (hiddenAt !== null) {
      hiddenTotal += performance.now() - hiddenAt;
      hiddenAt = null;
    }
  });
  const visibleNow = () => (hiddenAt ?? performance.now()) - hiddenTotal;
  const whenVisible = () =>
    document.hidden
      ? new Promise((resolve) => {
          const handler = () => {
            if (!document.hidden) {
              document.removeEventListener("visibilitychange", handler);
              resolve();
            }
          };
          document.addEventListener("visibilitychange", handler);
        })
      : Promise.resolve();
  const cancelled = new Error("cancelled");
  let generation = 0;
  const sleep = async (ms) => {
    const token = generation;
    const end = visibleNow() + ms;
    let left = ms;

    do {
      await whenVisible();
      if (left > 0) {
        await new Promise((resolve) => window.setTimeout(resolve, left));
      }
      if (token !== generation) {
        throw cancelled;
      }
      left = end - visibleNow();
    } while (left > 0);
  };

  const timing = {
    key: [45, 90],
    loginKey: [70, 110],
    printOk: [90, 220],
    print: [25, 110],
    afterType: 350,
    prompt: 900,
    effectPause: 2200,
    pause: 7200,
    lineDelay: 35,
    crt: 1500,
    boot: { idle: 2000, press: 600, start: 700, getty: 800, tty: 400, login: 1200, password: 4000, welcome: 1800, window: 700 },
    shutdown: { idle: 10000, broadcast: 1800, clear: 700, halt: 900, wipe: 180 },
    nms: { steps: 12, step: 50, hold: 1500, frame: 60 },
  };
  const jitter = ([min, spread]) => min + Math.random() * spread;
  const mean = ([min, spread]) => min + spread / 2;

  let html = "";
  let following = true;
  screen.addEventListener("scroll", () => {
    if (!screen.classList.contains("is-locked")) {
      following = screen.scrollHeight - screen.scrollTop - screen.clientHeight < 8;
    }
  });
  const render = (tail = cursor, force = false) => {
    following ||= force;
    screen.innerHTML = html + tail;
    if (following) {
      screen.scrollTop = screen.scrollHeight;
    }
  };
  const clearScreen = (tail = cursor) => {
    html = "";
    render(tail);
  };
  const fullscreen = async (effect) => {
    const token = generation;
    const top = screen.scrollTop;
    screen.classList.add("is-locked");
    screen.scrollTop = 0;

    try {
      await effect();
    } finally {
      if (token === generation) {
        resetScreen();
        screen.innerHTML = html;
        screen.scrollTop = following ? screen.scrollHeight : top;
      }
    }
  };

  const type = async (cmd, delay) => {
    html += markup(prompt);
    render();
    await sleep(delay);

    for (const char of cmd) {
      html += escapeHtml(char);
      render(cursor, true);
      await sleep(jitter(timing.key));
    }

    await sleep(timing.afterType);
    html += "\n";
  };

  const measureGrid = () => {
    const probe = document.createElement("span");
    probe.textContent = "M".repeat(100);
    screen.replaceChildren(probe);
    const charWidth = probe.getBoundingClientRect().width / 100;
    const style = getComputedStyle(screen);
    const charHeight = parseFloat(style.lineHeight);
    const innerWidth = screen.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    const innerHeight = screen.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);

    return {
      cols: Math.max(1, Math.floor(innerWidth / charWidth)),
      rows: Math.max(1, Math.floor(innerHeight / charHeight)),
    };
  };

  const cellsHtml = (cells) => {
    let line = "";
    let color = "";
    let run = "";
    const flush = () => {
      if (run) {
        line += color ? `<span class="${color}">${escapeHtml(run)}</span>` : escapeHtml(run);
      }
      run = "";
    };

    cells.forEach((cell) => {
      const next = cell?.color ?? "";

      if (next !== color) {
        flush();
        color = next;
      }

      run += cell?.char ?? " ";
    });
    flush();

    return line;
  };
  const blankGrid = (rows, cols) => Array.from({ length: rows }, () => Array(cols).fill(null));

  const animateGrid = async ({ duration = Infinity, interval, tight = false }, setup) => {
    screen.classList.toggle("is-tight", tight);
    const { cols, rows } = measureGrid();
    const draw = setup(cols, rows);
    const start = visibleNow();

    for (let frame = 0; visibleNow() - start < duration; frame += 1) {
      const grid = draw(blankGrid(rows, cols), frame, visibleNow() - start);

      if (!grid) {
        return;
      }

      screen.innerHTML = grid.map(cellsHtml).join("\n");
      await sleep(interval);
    }
  };

  const stamp = (grid, row, col, lines, color) => {
    lines.forEach((line, i) => {
      [...line].forEach((char, j) => {
        const r = row + i;
        const c = Math.round(col) + j;

        if (char !== " " && r >= 0 && r < grid.length && c >= 0 && c < grid[0].length) {
          grid[r][c] = { char, color };
        }
      });
    });
  };

  const matrix = (duration) =>
    animateGrid({ duration, interval: 60 }, (cols, rows) => {
      const glyphs = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*+=<>?";
      const randomGlyph = () => glyphs[Math.floor(Math.random() * glyphs.length)];
      const chars = Array.from({ length: rows }, () => Array.from({ length: cols }, randomGlyph));
      const newDrop = (start) => ({
        y: start ? -Math.random() * rows * 2 : -Math.random() * rows,
        speed: 0.3 + Math.random() * 0.7,
        length: 4 + Math.floor(Math.random() * rows),
      });
      const drops = Array.from({ length: cols }, () => newDrop(true));

      return (grid) => {
        drops.forEach((drop, col) => {
          for (let row = 0; row < rows; row += 1) {
            const distance = Math.floor(drop.y) - row;
            let color = "";

            if (distance === 0) {
              color = "term-matrix-head";
            } else if (distance > 0 && distance < drop.length) {
              color = distance < drop.length / 2 ? "term-green" : "term-matrix-dim";
            }

            if (color) {
              if (Math.random() < 0.05) {
                chars[row][col] = randomGlyph();
              }
              grid[row][col] = { char: chars[row][col], color };
            }
          }

          drop.y += drop.speed;

          if (drop.y - drop.length > rows) {
            drops[col] = newDrop(false);
          }
        });

        return grid;
      };
    });

  const locomotive = [
    "      ====        ________                ___________ ",
    "  _D _|  |_______/        \\__I_I_____===__|_________| ",
    "   |(_)---  |   H\\________/ |   |        =|___ ___|   ",
    "   /     |  |   H  |  |     |   |         ||_| |_||   ",
    "  |      |  |   H  |__--------------------| [___] |   ",
    "  | ________|___H__/__|_____/[][]~\\_______|       |   ",
    "  |/ |   |-----------I_____I [][] []  D   |=======|__ ",
  ];
  const wheels = [
    [
      "__/ =| o |=-~~\\  /~~\\  /~~\\  /~~\\ ____Y___________|__ ",
      " |/-=|___|=    ||    ||    ||    |_____/~\\___/        ",
      "  \\_/      \\O=====O=====O=====O_/      \\_/            ",
    ],
    [
      "__/ =| o |=-~~\\  /~~\\  /~~\\  /~~\\ ____Y___________|__ ",
      " |/-=|___|=O=====O=====O=====O   |_____/~\\___/        ",
      "  \\_/      \\__/  \\__/  \\__/  \\__/      \\_/            ",
    ],
    [
      "__/ =| o |=-O=====O=====O=====O \\ ____Y___________|__ ",
      " |/-=|___|=    ||    ||    ||    |_____/~\\___/        ",
      "  \\_/      \\__/  \\__/  \\__/  \\__/      \\_/            ",
    ],
  ];
  const coal = [
    "                              ",
    "                              ",
    "    _________________         ",
    "   _|                \\_____A  ",
    " =|                        |  ",
    " -|                        |  ",
    "__|________________________|_ ",
    "|__________________________|_ ",
    "   |_D__D__D_|  |_D__D__D_|   ",
    "    \\_/   \\_/    \\_/   \\_/    ",
  ];
  const smoke = [
    ["                 (@@) (  ) (@)  ( )  @@    ()    @     O     @", "            (   )", "        (@@@@)", "     (    )", "", "   (@@@)"],
    ["                 (  ) (@@) ( )  (@)  ()    @@    O     @     O", "            (@@@)", "        (    )", "     (@@@@)", "", "   (   )"],
  ];

  const trainWidth = locomotive[0].length + coal[0].length;

  const train = () =>
    animateGrid({ interval: 40 }, (cols, rows) => {
      const smokeRows = Math.max(0, Math.min(smoke[0].length, rows - coal.length));
      const top = Math.max(0, Math.floor((rows - smokeRows - coal.length) / 2));

      return (grid, frame) => {
        const x = cols - frame;

        if (x <= -trainWidth) {
          return null;
        }

        const body = [...locomotive, ...wheels[((x % 3) + 3) % 3]].map((line, i) => line + coal[i]);
        const puff = smoke[Math.floor(x / 4) % 2 === 0 ? 0 : 1];
        stamp(grid, top, x, [...puff.slice(puff.length - smokeRows), ...body]);

        return grid;
      };
    });

  const pipes = (duration) =>
    animateGrid({ duration, interval: 30, tight: true }, (cols, rows) => {
      const colors = ["term-green", "term-blue", "term-yellow", "term-red", "term-magenta", "term-cyan"];
      const straight = ["┃", "━", "┃", "━"];
      const corners = {
        "0-1": "┏", "0-3": "┓", "2-1": "┗", "2-3": "┛",
        "1-0": "┛", "1-2": "┓", "3-0": "┗", "3-2": "┏",
      };
      const steps = [[-1, 0], [0, 1], [1, 0], [0, -1]];
      const randomColor = () => colors[Math.floor(Math.random() * colors.length)];
      const newPipe = () => ({
        row: Math.floor(Math.random() * rows),
        col: Math.floor(Math.random() * cols),
        dir: Math.floor(Math.random() * 4),
        color: randomColor(),
      });
      let grid = blankGrid(rows, cols);
      let drawn = 0;
      const active = [newPipe(), newPipe()];

      return () => {
        active.forEach((pipe) => {
          let next = pipe.dir;

          if (Math.random() < 0.13) {
            next = (pipe.dir + (Math.random() < 0.5 ? 1 : 3)) % 4;
          }

          grid[pipe.row][pipe.col] = {
            char: next === pipe.dir ? straight[next] : corners[`${pipe.dir}-${next}`],
            color: pipe.color,
          };
          drawn += 1;
          pipe.dir = next;
          pipe.row += steps[next][0];
          pipe.col += steps[next][1];

          if (pipe.row < 0 || pipe.row >= rows || pipe.col < 0 || pipe.col >= cols) {
            pipe.row = (pipe.row + rows) % rows;
            pipe.col = (pipe.col + cols) % cols;
            pipe.color = randomColor();
          }
        });

        if (drawn > rows * cols * 0.7) {
          grid = blankGrid(rows, cols);
          drawn = 0;
        }

        return grid;
      };
    });

  const bonsai = async (hold) => {
    await animateGrid({ interval: 45 }, (cols, rows) => {
      const pot = [
        ":_______________________:",
        " \\_____________________/",
        "  (_)               (_)",
      ];
      const grid = blankGrid(rows, cols);
      const center = Math.floor(cols / 2);
      const potTop = rows - pot.length;
      const potLeft = center - Math.floor(pot[0].length / 2);
      const random = (min, max) => min + Math.floor(Math.random() * (max - min + 1));
      const put = (row, col, char, color) => {
        if (row < 0 || row >= potTop || col < 0 || col >= cols) {
          return;
        }

        if (char === "&" && grid[row][col] && grid[row][col].char !== "&") {
          return;
        }

        grid[row][col] = { char, color };
      };

      pot.forEach((line, i) =>
        [...line].forEach((char, j) => {
          if (char !== " " && potLeft + j >= 0 && potLeft + j < cols) {
            grid[potTop + i][potLeft + j] = { char, color: "term-gray" };
          }
        }),
      );

      const trunkLife = Math.max(10, potTop + 4);
      const woodChar = (dx, dy) => {
        if (dy === 0) {
          return Math.random() < 0.5 ? "_" : "~";
        }
        if (dx < 0) {
          return "\\";
        }
        return dx > 0 ? "/" : "|";
      };
      let branches = [{ row: potTop - 1, col: center, type: "trunk", life: trunkLife, age: 0 }];
      let ticks = 0;

      return () => {
        if (!branches.length || ticks >= 400) {
          return null;
        }

        const spawned = [];

        branches.forEach((branch) => {
          branch.life -= 1;
          branch.age += 1;
          let dx = 0;
          let dy = 0;

          if (branch.type === "leaf" || branch.life < 4) {
            dx = random(-2, 2);
            dy = random(-1, 0);
            put(branch.row, branch.col, "&", "term-green");

            if (branch.type !== "leaf") {
              for (let i = 0; i < 2 && branches.length + spawned.length < 140; i += 1) {
                spawned.push({ row: branch.row, col: branch.col, type: "leaf", life: random(3, 6), age: 0 });
              }
            }
          } else {
            if (branch.type === "trunk") {
              dy = branch.age < 3 || Math.random() < 0.6 ? -1 : 0;
              dx = Math.random() < 0.55 ? 0 : random(-1, 1);
            } else {
              dx = (branch.type === "left" ? -1 : 1) * (Math.random() < 0.3 ? 2 : 1);
              dy = Math.random() < 0.4 ? -1 : 0;
            }

            const char = woodChar(dx, dy);
            put(branch.row, branch.col, char, "term-yellow");

            if (Math.abs(dx) === 2 && dy === 0) {
              put(branch.row, branch.col + dx / 2, char, "term-yellow");
            }

            const chance = branch.type === "trunk" ? 0.3 : 0.15;
            if (branch.age > 3 && branches.length + spawned.length < 140 && Math.random() < chance) {
              spawned.push({
                row: branch.row,
                col: branch.col,
                type: branch.type === "trunk" ? (Math.random() < 0.5 ? "left" : "right") : branch.type,
                life: random(6, 12),
                age: 0,
              });
            }
          }

          branch.row = Math.min(potTop - 1, Math.max(0, branch.row + dy));
          branch.col = Math.min(cols - 1, Math.max(0, branch.col + dx));
        });

        branches = [...branches.filter((branch) => branch.life > 0), ...spawned];
        ticks += 1;

        return grid;
      };
    });

    await sleep(hold);
  };

  const fishColors = ["term-green", "term-blue", "term-yellow", "term-red", "term-magenta", "term-cyan"];
  const pick = (items) => items[Math.floor(Math.random() * items.length)];

  const aquarium = (duration) =>
    animateGrid({ duration, interval: 70 }, (cols, rows) => {
      const waves = [
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
        "^^^^ ^^^  ^^^   ^^^    ^^^^      ^^^  ^^",
        "  ^^^^      ^^^^     ^^^    ^^     ^^^^ ",
        "^^      ^^^^      ^^^    ^^^^^^         ",
      ];
      const kinds = [
        { right: ["><>"], left: ["<><"] },
        { right: ["><((('>"], left: ["<')))><"] },
        { right: ["  __", "\\/ o\\", "/\\__/"], left: [" __", "/o \\/", "\\__/\\"] },
      ];
      const top = waves.length + 1;
      const newFish = (anywhere) => {
        const kind = pick(kinds);
        const dir = Math.random() < 0.5 ? 1 : -1;
        const art = dir > 0 ? kind.right : kind.left;
        const width = Math.max(...art.map((line) => line.length));
        return {
          art,
          dir,
          width,
          row: top + Math.floor(Math.random() * Math.max(1, rows - top - art.length - 2)),
          col: anywhere ? Math.random() * cols : dir > 0 ? -width : cols,
          speed: 0.25 + Math.random() * 0.6,
          color: pick(fishColors),
        };
      };
      const fish = Array.from({ length: Math.max(4, Math.floor((rows * cols) / 220)) }, () => newFish(true));
      const sharkRight = [
        "          __        ",
        "         /  |       ",
        " \\  ____/   |____   ",
        "  >(____________ o`-.",
        " /     \\  \\______vvv/",
      ];
      const mirror = { "/": "\\", "\\": "/", "(": ")", ")": "(", "<": ">", ">": "<", "`": "'", "'": "`" };
      const sharkLeft = sharkRight.map((line) =>
        [...line.padEnd(21)]
          .reverse()
          .map((char) => mirror[char] ?? char)
          .join(""),
      );
      const newShark = () => {
        const dir = Math.random() < 0.5 ? 1 : -1;
        return {
          dir,
          art: dir > 0 ? sharkRight : sharkLeft,
          col: dir > 0 ? -22 : cols + 1,
          row: top + 1 + Math.floor(Math.random() * Math.max(1, rows - top - sharkRight.length - 6)),
          wait: 15 + Math.floor(Math.random() * 30),
        };
      };
      let shark = newShark();
      const weeds = Array.from({ length: Math.max(2, Math.floor(cols / 12)) }, () => ({
        col: Math.floor(Math.random() * (cols - 2)),
        height: 3 + Math.floor(Math.random() * Math.max(1, Math.min(5, rows / 4))),
      }));
      let bubbles = [];

      return (grid, frame) => {
        waves.forEach((wave, r) => {
          const shift = Math.floor(frame / (3 + r)) * (r % 2 === 0 ? 1 : -1);
          for (let c = 0; c < cols; c += 1) {
            const char = wave[(((c + shift) % wave.length) + wave.length) % wave.length];
            if (char !== " ") {
              grid[r][c] = { char, color: r === 0 ? "term-cyan" : "term-blue" };
            }
          }
        });

        weeds.forEach((weed) => {
          for (let i = 0; i < weed.height; i += 1) {
            const sway = (i + Math.floor(frame / 8)) % 2;
            stamp(grid, rows - 1 - i, weed.col + sway, [sway ? ")" : "("], "term-green");
          }
        });

        bubbles.forEach((bubble) => {
          bubble.row -= 0.3;
          stamp(grid, Math.round(bubble.row), bubble.col, [bubble.row < top + 3 ? "O" : "o"], "term-cyan");
        });
        bubbles = bubbles.filter((bubble) => bubble.row > waves.length);

        fish.forEach((one, i) => {
          one.col += one.dir * one.speed;

          if (one.col > cols + 1 || one.col < -one.width - 1) {
            fish[i] = newFish(false);
            return;
          }

          if (Math.random() < 0.02) {
            bubbles.push({ row: one.row, col: Math.round(one.dir > 0 ? one.col + one.width : one.col - 1) });
          }

          stamp(grid, one.row, one.col, one.art, one.color);
        });

        if (shark.wait > 0) {
          shark.wait -= 1;
        } else {
          shark.col += shark.dir * 0.7;
          stamp(grid, shark.row, shark.col, shark.art, "term-gray");

          if (shark.col > cols + 2 || shark.col < -24) {
            shark = newShark();
          }
        }

        return grid;
      };
    });

  const robotSprite = [
    "........kk..........",
    ".......krrk.........",
    "........kk..........",
    "........kk..........",
    "..kkkkkkkkkkkkkkk...",
    ".kgggggggggggggggk..",
    "kgglllllllllllllggk.",
    "kgglkkkkkkkkkkklggk.",
    "kgglkccwkkkccwklggkk",
    "kgglkcckkkkcckklggkg",
    "kgglkkkkkkkkkkklggkk",
    "kgglkkkcccccckklggk.",
    "kgglllllllllllllggk.",
    ".kgggggggggggggggk..",
    "..kkkkkkkkkkkkkkk...",
    "....kdddk...kdddk...",
    "....kdddk...kdddk...",
    ".....kyk.....kyk....",
  ];
  const robotPalette = {
    k: "nyan-outline",
    g: "nyan-body",
    l: "nyan-light",
    d: "nyan-shade",
    c: "nyan-eye",
    w: "nyan-white",
    r: "nyan-red",
    y: "nyan-yellow",
    o: "nyan-orange",
  };
  const sparkles = [
    ["...", ".w.", "..."],
    [".w.", "www", ".w."],
    ["..w..", "..w..", "ww.ww", "..w..", "..w.."],
    [".w.w.", "w...w", ".....", "w...w", ".w.w."],
  ];

  const nyancat = async (duration) => {
    const canvas = document.createElement("canvas");
    screen.classList.add("is-canvas");
    screen.replaceChildren(canvas);
    const width = screen.clientWidth;
    const height = screen.clientHeight;
    const ratio = window.devicePixelRatio || 1;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    const context = canvas.getContext("2d");
    context.scale(ratio, ratio);
    const themeStyle = getComputedStyle(document.documentElement);
    const color = (name) => themeStyle.getPropertyValue(`--color-${name}`).trim();
    const palette = Object.fromEntries(Object.entries(robotPalette).map(([key, name]) => [key, color(name)]));
    const fontFamily = getComputedStyle(screen).fontFamily;
    const sky = color("nyan-sky");
    const starPalette = { w: color("nyan-star") };
    const text = color("nyan-text");

    const size = Math.max(3, Math.floor(height / 48));
    const cols = Math.ceil(width / size);
    const rows = Math.ceil(height / size);
    const bands = [1, 2, 3, 4, 5, 6].map((index) => color(`nyan-band-${index}`));
    const band = 2;
    const robotCol = Math.min(Math.floor(cols * 0.52), cols - robotSprite[0].length - 2);
    const stars = Array.from({ length: Math.max(6, Math.floor(cols / 14)) }, () => ({
      col: Math.random() * cols,
      row: Math.floor(Math.random() * rows),
      phase: Math.floor(Math.random() * sparkles.length),
    }));
    const pixel = (col, row, fill) => {
      context.fillStyle = fill;
      context.fillRect(col * size, row * size, size, size);
    };
    const sprite = (lines, col, row, palette) => {
      lines.forEach((line, i) =>
        [...line].forEach((key, j) => {
          if (palette[key]) {
            pixel(col + j, row + i, palette[key]);
          }
        }),
      );
    };
    const start = visibleNow();
    let frame = 0;

    while (visibleNow() - start < duration) {
      context.fillStyle = sky;
      context.fillRect(0, 0, width, height);

      stars.forEach((star) => {
        star.col -= 1.5;
        if (star.col < -6) {
          star.col = cols + 2;
          star.row = Math.floor(Math.random() * rows);
        }
        const shape = sparkles[(star.phase + Math.floor(frame / 3)) % sparkles.length];
        sprite(shape, Math.round(star.col), star.row, starPalette);
      });

      const bob = Math.floor(frame / 4) % 2;
      const robotRow = Math.floor(rows / 2) - Math.floor(robotSprite.length / 2) + bob;
      const trailTop = robotRow + 5;

      for (let col = 0; col < robotCol + 2; col += 1) {
        const wave = Math.floor((col + frame) / 8) % 2;
        bands.forEach((fill, i) => {
          for (let k = 0; k < band; k += 1) {
            pixel(col, trailTop + i * band + k - wave, fill);
          }
        });
      }

      sprite(robotSprite, robotCol, robotRow, palette);
      [6, 14].forEach((offset) => {
        pixel(robotCol + offset, robotRow + robotSprite.length, palette.o);
        if (frame % 2 === 0) {
          pixel(robotCol + offset, robotRow + robotSprite.length + 1, palette.y);
        }
      });

      const message = `You have nyaned for ${Math.floor((visibleNow() - start) / 1000)} seconds!`;
      let fontSize = Math.max(11, size * 2);
      context.font = `${fontSize}px ${fontFamily}`;
      while (fontSize > 8 && context.measureText(message).width > width - 16) {
        fontSize -= 1;
        context.font = `${fontSize}px ${fontFamily}`;
      }
      context.fillStyle = text;
      context.textAlign = "center";
      context.textBaseline = "bottom";
      context.fillText(message, width / 2, height - size);

      frame += 1;
      await sleep(70);
    }
  };

  const aafire = (duration) =>
    animateGrid({ duration, interval: 60, tight: true }, (cols, rows) => {
      const palette = " .:-=+*#%@";
      const colors = ["", "term-fire-1", "term-fire-1", "term-fire-2", "term-fire-2", "term-fire-3", "term-fire-3", "term-fire-4", "term-fire-4", "term-fire-5"];
      const max = 1;
      const decay = (2 * max) / (rows * 0.8);
      const heat = Array.from({ length: rows }, () => new Float32Array(cols));

      return (grid) => {
        for (let c = 0; c < cols; c += 1) {
          heat[rows - 1][c] = Math.random() < 0.85 ? max * (0.75 + Math.random() * 0.25) : 0;
        }

        for (let r = 1; r < rows; r += 1) {
          for (let c = 0; c < cols; c += 1) {
            const shift = Math.floor(Math.random() * 3) - 1;
            const target = Math.min(cols - 1, Math.max(0, c + shift));
            heat[r - 1][target] = Math.max(0, heat[r][c] - Math.random() * decay);
          }
        }

        for (let r = 0; r < rows; r += 1) {
          for (let c = 0; c < cols; c += 1) {
            const level = Math.min(palette.length - 1, Math.floor((heat[r][c] / max) * palette.length));
            if (level > 0) {
              grid[r][c] = { char: palette[level], color: colors[level] };
            }
          }
        }

        return grid;
      };
    });

  const nms = async (session) => {
    const lines = outputLines(session).map((line) => [...line]);
    const base = html;
    const glyph = () => String.fromCharCode(33 + Math.floor(Math.random() * 94));
    const reveal = option(session, "duration");
    const revealAt = lines.map((chars) => chars.map(() => Math.random() * reveal));
    const total = lines.reduce((sum, chars) => sum + chars.length, 0);
    const { steps, step, hold, frame } = timing.nms;
    const draw = (shown, elapsed) => {
      let count = 0;
      const body = lines
        .map((chars, row) =>
          cellsHtml(
            chars.flatMap((char, col) => {
              count += 1;

              if (count > shown) {
                return [];
              }

              const decrypted = char === " " || elapsed >= revealAt[row][col];
              return [{ char: decrypted ? char : glyph(), color: decrypted && char !== " " ? option(session, "color") : "" }];
            }),
          ),
        )
        .join("\n");
      html = `${base}${body}\n`;
      render("");
    };

    for (let index = 1; index <= steps; index += 1) {
      draw(Math.ceil((total * index) / steps), -1);
      await sleep(step);
    }

    await sleep(hold);
    const start = visibleNow();

    while (visibleNow() - start < reveal) {
      draw(total, visibleNow() - start);
      await sleep(frame);
    }

    draw(total, reveal);
  };

  const effects = {
    sl: { run: () => train(), estimate: (session, cols) => (cols + trainWidth) * 44 },
    pipes: { duration: 12000, run: (session) => pipes(option(session, "duration")) },
    cbonsai: {
      hold: 4000,
      run: (session) => bonsai(option(session, "hold")),
      estimate: (session) => 2500 + option(session, "hold"),
    },
    asciiquarium: { duration: 12000, run: (session) => aquarium(option(session, "duration")) },
    nyancat: { duration: 10000, run: (session) => nyancat(option(session, "duration")) },
    aafire: { duration: 10000, run: (session) => aafire(option(session, "duration")) },
    cmatrix: { duration: 8000, run: (session) => matrix(option(session, "duration")) },
    nms: {
      inline: true,
      duration: 3000,
      color: "term-blue",
      run: (session) => nms(session),
      estimate: (session) => timing.nms.steps * timing.nms.step + timing.nms.hold + option(session, "duration"),
    },
  };
  const option = (session, key) => session[key] ?? effects[session.effect]?.[key];

  const printLines = async (lines = []) => {
    for (const line of lines) {
      html += `${markup(line)}\n`;
      render("");
      await sleep(jitter(line.includes("OK") ? timing.printOk : timing.print));
    }
  };

  const timestamp = () => {
    const now = new Date();
    const pad = (value) => String(value).padStart(2, "0");
    const zone = new Intl.DateTimeFormat("en-US", { timeZoneName: "short" }).formatToParts(now).find((part) => part.type === "timeZoneName")?.value ?? "UTC";
    const day = now.toLocaleDateString("en-US", { weekday: "short" });
    return `${day} ${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())} ${zone}`;
  };

  const crtFlash = async (mode, wipe = 0) => {
    const crt = document.createElement("div");
    const height = screen.offsetHeight;
    crt.className = `terminal-crt is-${mode}`;
    crt.style.top = `${screen.offsetTop + height / 2}px`;
    crt.style.setProperty("--crt-height", `${height}px`);
    terminal.append(crt);
    setBooting(true);

    await sleep(wipe);
    clearScreen("");
    await sleep(timing.crt - wipe);
    crt.remove();
  };

  const boot = async (settings) => {
    await crtFlash("on");
    await sleep(timing.boot.start);

    await printLines(settings.lines);
    await sleep(timing.boot.getty);
    clearScreen("");
    await sleep(timing.boot.tty);

    html += `${escapeHtml(settings.issue ?? "")}\n\n${escapeHtml(settings.login ?? "login: ")}`;
    render();
    await sleep(timing.boot.login);

    for (const char of settings.user ?? "") {
      html += escapeHtml(char);
      render();
      await sleep(jitter(timing.loginKey));
    }

    html += "\nPassword: ";
    render();
    await sleep(timing.boot.password);
    html += `\n\n${escapeHtml(settings.welcome ?? "")}\n`;
    render("");
    await sleep(timing.boot.welcome);

    setBooting(false);
    clearScreen();
    await sleep(timing.boot.window);
  };

  const nextDelay = (session) =>
    session.pause ?? (effects[session.effect] ? timing.effectPause : timing.pause);
  const matrixSession = config.matrix && { cmd: "cmatrix", ...config.matrix, effect: "cmatrix" };

  const sessionHtml = (session) => {
    const lines = outputLines(session);
    const body = effects[session.effect]?.inline
      ? lines
          .map((line) => cellsHtml([...line].map((char) => ({ char, color: char === " " ? "" : option(session, "color") }))) + "\n")
          .join("")
      : lines.map((line, index) => outputHtml(session, line, index)).join("");
    return `${markup(prompt)}${escapeHtml(session.cmd)}\n${body}`;
  };

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setBooting(false);
    screen.innerHTML = sessions.map(sessionHtml).join("") + markup(prompt) + cursor;
    return;
  }

  const runSession = async (session, delay) => {
    const effect = effects[session.effect];
    await type(session.cmd, delay);

    if (effect?.inline) {
      await effect.run(session);
      return;
    }

    if (effect) {
      await fullscreen(() => effect.run(session));
    }

    for (const [index, line] of outputLines(session).entries()) {
      html += outputHtml(session, line, index);
      render("");
      await sleep(session.lineDelay ?? timing.lineDelay);
    }
  };

  const shutdown = async (settings, wait) => {
    await type(settings.cmd ?? "shutdown -h now", wait);

    if (settings.broadcast) {
      html += `\n${markup(settings.broadcast.replace("{now}", timestamp())).replace(/\n+$/, "")}\n`;
      render("");
      await sleep(timing.shutdown.broadcast);
    }

    setBooting(true);
    clearScreen("");
    await sleep(timing.shutdown.clear);
    await printLines(settings.lines);
    await sleep(timing.shutdown.halt);
    await crtFlash("off", timing.shutdown.wipe);
  };

  const { cols } = measureGrid();
  screen.replaceChildren();
  const typing = (cmd, wait) => wait + cmd.length * mean(timing.key) + timing.afterType;
  const printing = (lines = []) =>
    lines.reduce((total, line) => total + mean(line.includes("OK") ? timing.printOk : timing.print), 0);
  const sessionTime = (session, wait) => {
    const effect = effects[session.effect];
    const effectTime = effect ? (effect.estimate?.(session, cols) ?? option(session, "duration")) : 0;
    const outputTime = effect?.inline ? 0 : outputLines(session).length * (session.lineDelay ?? timing.lineDelay);
    return typing(session.cmd, wait) + effectTime + outputTime;
  };
  const sessionStep = (session, wait, chained) => ({
    label: session.cmd,
    wait,
    chained,
    estimate: sessionTime(session, wait),
    run: (delay) => runSession(session, delay),
    after: (previous) => previous + sessionHtml(session),
  });

  const steps = [];

  if (config.boot) {
    const settings = config.boot;
    const { start, getty, tty, login, password, welcome, window: show } = timing.boot;
    steps.push({
      label: "boot",
      wait: 0,
      estimate: timing.crt + start + getty + tty + printing(settings.lines) + login + (settings.user ?? "").length * mean(timing.loginKey) + password + welcome + show,
      run: () => boot(settings),
      after: () => "",
    });
  }

  let pause = timing.prompt;
  sessions.forEach((session) => {
    steps.push(sessionStep(session, pause, true));
    pause = nextDelay(session);
  });

  const clearWait = pause + (config.clearDelay ?? 0);
  steps.push({
    label: "clear",
    wait: clearWait,
    chained: true,
    estimate: typing("clear", clearWait),
    run: async (delay) => {
      await type("clear", delay);
      clearScreen();
    },
    after: () => "",
  });

  if (matrixSession) {
    const step = sessionStep(matrixSession, timing.prompt, false);
    steps.push({
      ...step,
      run: async (delay) => {
        await step.run(delay);
        clearScreen("");
      },
      after: () => "",
    });
  }

  if (config.goodbye) {
    steps.push(sessionStep(config.goodbye, timing.prompt, false));
  }

  if (config.shutdown) {
    const settings = config.shutdown;
    const { idle, broadcast, clear, halt } = timing.shutdown;
    const wait = settings.idle ?? idle;
    steps.push({
      label: settings.cmd ?? "shutdown -h now",
      wait,
      estimate:
        typing(settings.cmd ?? "shutdown -h now", wait) + (settings.broadcast ? broadcast : 0) + clear + printing(settings.lines) + halt + timing.crt,
      run: (delay) => shutdown(settings, delay),
      after: () => "",
    });
  }

  const power = document.querySelector("[data-terminal-power]");
  const showPower = (visible) => {
    if (power) {
      power.hidden = !visible;
      power.classList.remove("is-pressed");
    }
  };

  const progress = () => {
    const container = document.querySelector("[data-terminal-progress]");
    const track = container?.querySelector("[data-terminal-track]");
    const eta = container?.querySelector("[data-terminal-eta]");
    let index = 0;
    let started = 0;
    let timer = null;

    if (!container || !track || !config.shutdown) {
      return { start: () => {}, off: () => {} };
    }

    const fills = steps.map((step, position) => {
      const button = document.createElement("button");
      const fill = document.createElement("span");
      button.type = "button";
      button.className = "terminal-step";
      button.title = step.label;
      button.setAttribute("aria-label", `Jump to ${step.label}`);
      button.style.setProperty("--weight", String(Math.round(step.estimate)));
      button.addEventListener("click", () => seek(position));
      fill.className = "terminal-step-fill";
      button.append(fill);
      track.append(button);
      return fill;
    });
    const format = (ms) => {
      const seconds = Math.ceil(Math.max(0, ms) / 1000);
      return `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")} remaining`;
    };
    const show = () => {
      const elapsed = visibleNow() - started;
      const remaining =
        steps.slice(index + 1).reduce((total, step) => total + step.estimate, 0) + Math.max(0, (steps[index]?.estimate ?? 0) - elapsed);
      fills.forEach((fill, position) => {
        const ratio = position < index ? 1 : position > index ? 0 : Math.min(1, elapsed / steps[position].estimate);
        fill.style.setProperty("--fill", `${(ratio * 100).toFixed(1)}%`);
      });
      if (eta) {
        eta.textContent = index >= 0 && index < steps.length ? format(remaining) : "powered off";
      }
    };

    container.hidden = false;

    return {
      start: (position, skipped) => {
        index = position;
        started = visibleNow() - skipped;
        show();
        timer ??= window.setInterval(show, 250);
      },
      off: (finished) => {
        window.clearInterval(timer);
        timer = null;
        index = finished ? steps.length : -1;
        show();
      },
    };
  };

  const clock = progress();
  const firstSession = config.boot ? 1 : 0;

  const unlessCancelled = async (task) => {
    try {
      await task();
    } catch (error) {
      if (error !== cancelled) {
        throw error;
      }
    }
  };

  const play = (from, seeked) =>
    unlessCancelled(async () => {
      for (let position = from; ; position = firstSession) {
        for (let index = position; index < steps.length; index += 1) {
          const step = steps[index];
          const delay = seeked && index === from && step.chained ? timing.prompt : step.wait;
          clock.start(index, step.wait - delay);
          await step.run(delay);
        }

        if (config.shutdown) {
          clock.off(true);
          showPower(true);
          return;
        }
      }
    });

  const seek = (index) => {
    generation += 1;
    showPower(false);
    terminal?.querySelector(".terminal-crt")?.remove();
    resetScreen();
    setBooting(false);
    html = steps.slice(0, index).reduce((previous, step) => step.after(previous), "");
    render(cursor, true);
    play(index, true);
  };

  const powerUp = () =>
    unlessCancelled(async () => {
      if (config.boot && power) {
        showPower(true);
        clock.off(false);
        await sleep(timing.boot.idle);
        power.classList.add("is-pressed");
        await sleep(timing.boot.press);
        showPower(false);
      }
      play(0, false);
    });

  power?.addEventListener("click", () => seek(0));
  powerUp();
};

const initializeEventBindings = () => {
  document.querySelectorAll("[data-accordion-trigger]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const targetSelector = trigger.dataset.accordionTarget;
      const target = targetSelector
        ? trigger.closest(targetSelector) ?? document.querySelector(targetSelector)
        : trigger.closest("[data-accordion-item]") ?? trigger;

      expandAccordion(target);
    });
  });

  document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
    toggle.addEventListener("mousedown", (event) => event.preventDefault());
    toggle.addEventListener("click", () => {
      window.toggleTheme();
    });
  });
};

window.toggleTheme = () => {
  setTheme(html.classList.contains("dark") ? "light" : "dark");
};

setTheme(getPreferredTheme());

window.addEventListener("DOMContentLoaded", () => {
  fixThemeToggleIcon(html.classList.contains("dark") ? "dark" : "light");
  initializeEventBindings();
  initializePostNavigation();
  syncActiveAccordionPanel();
  initializeSkillBars();
  initializeSearch();
  initializeTerminal();
});
