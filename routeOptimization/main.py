from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import heapq
import sys
import re


# =================== Structures ===================

@dataclass
class Edge:
    to: int
    dist: int
    time: int
    cost: int


class Graph:
    def __init__(self) -> None:
        # id -> list[Edge]
        self.adj: Dict[int, List[Edge]] = {}

    def add_city(self, city_id: int) -> None:
        if city_id not in self.adj:
            self.adj[city_id] = []

    def add_road(self, id1: int, id2: int, distance: int, t: int, c: int) -> None:
        self.add_city(id1)
        self.add_city(id2)
        self.adj[id1].append(Edge(id2, distance, t, c))
        self.adj[id2].append(Edge(id1, distance, t, c))

    def dijkstra(
        self,
        start: int,
        end: int,
        mode: str,
        weights: Optional[Dict[str, int]] = None
    ) -> Tuple[List[int], Dict[str, int]]:
        """
        mode: 'D', 'V', 'C' or 'COMBO'
        weights: only for 'COMBO', keys 'D','V','C'
        """
        INF = 10**18
        n_nodes = len(self.adj)
        # dist only for priority queue
        best: Dict[int, int] = {v: INF for v in self.adj.keys()}
        prev: Dict[int, Optional[int]] = {v: None for v in self.adj.keys()}

        # store true sums to avoid recomputing later
        sumD: Dict[int, int] = {v: 0 for v in self.adj.keys()}
        sumV: Dict[int, int] = {v: 0 for v in self.adj.keys()}
        sumC: Dict[int, int] = {v: 0 for v in self.adj.keys()}

        best[start] = 0
        heap: List[Tuple[int, int]] = [(0, start)]

        while heap:
            cur_w, v = heapq.heappop(heap)
            if cur_w != best[v]:
                continue
            if v == end:
                break
            for e in self.adj[v]:
                if mode == "D":
                    w = cur_w + e.dist
                elif mode == "V":
                    w = cur_w + e.time
                elif mode == "C":
                    w = cur_w + e.cost
                elif mode == "COMBO":
                    w = (
                        cur_w
                        + weights["D"] * e.dist
                        + weights["V"] * e.time
                        + weights["C"] * e.cost
                    )
                else:
                    raise ValueError("Unknown mode")

                if w < best[e.to]:
                    best[e.to] = w
                    prev[e.to] = v
                    # update accumulated sums based on previous node
                    sumD[e.to] = sumD[v] + e.dist
                    sumV[e.to] = sumV[v] + e.time
                    sumC[e.to] = sumC[v] + e.cost
                    heapq.heappush(heap, (w, e.to))

        if best[end] == INF:
            return [], {"D": 0, "V": 0, "C": 0}

        # reconstruct path
        path_ids: List[int] = []
        cur = end
        while cur is not None:
            path_ids.append(cur)
            cur = prev[cur]
        path_ids.reverse()
        return path_ids, {"D": sumD[end], "V": sumV[end], "C": sumC[end]}


# =================== Parsing ===================

def parse_input(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    section = None
    graph = Graph()
    id_to_name: Dict[int, str] = {}
    name_to_id: Dict[str, int] = {}
    requests: List[Dict[str, object]] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line.upper()
            continue

        if section == "[CITIES]":
            # Format: ID: Name with spaces
            # split only at first colon
            parts = line.split(":", 1)
            if len(parts) != 2:
                continue
            cid = int(parts[0].strip())
            cname = parts[1].strip()
            id_to_name[cid] = cname
            name_to_id[cname] = cid
            graph.add_city(cid)

        elif section == "[ROADS]":
            # Format: ID1 - ID2: d, t, c
            # Extract left and right of colon
            left, right = line.split(":", 1)
            # left: "ID1 - ID2"
            lr = left.split("-")
            id1 = int(lr[0].strip())
            id2 = int(lr[1].strip())
            # right: "d, t, c"
            nums = [x.strip() for x in right.split(",")]
            d = int(nums[0])
            t = int(nums[1])
            c = int(nums[2])
            graph.add_road(id1, id2, d, t, c)

        elif section == "[REQUESTS]":
            # Format: City_from -> City_to | (Д,В,С)
            # split by '|'
            if "|" not in line:
                continue
            left, right = line.split("|", 1)
            left = left.strip()
            right = right.strip()
            # left: city_from -> city_to
            lr = left.split("->")
            city_from = lr[0].strip()
            city_to = lr[1].strip()
            # right: (Д,В,С)
            m = re.search(r"\(([^)]*)\)", right)
            if not m:
                continue
            prio_str = m.group(1)
            prios = [p.strip() for p in prio_str.split(",")]
            requests.append(
                {
                    "from_name": city_from,
                    "to_name": city_to,
                    "priorities": prios,
                }
            )

    return graph, id_to_name, name_to_id, requests


# =================== Routing Logic ===================

def priorities_to_weights(prios: List[str]) -> Dict[str, int]:
    """
    prios: e.g. ['Д', 'В', 'С']
    Higher position -> higher weight.
    """
    # 3,2,1
    base = [3, 2, 1]
    mapping = {"Д": "D", "В": "V", "С": "C"}
    weights = {"D": 1, "V": 1, "C": 1}
    for idx, symbol in enumerate(prios):
        if symbol in mapping:
            k = mapping[symbol]
            weights[k] = base[idx]
    return weights


def build_routes_for_request(
    graph: Graph,
    id_to_name: Dict[int, str],
    name_to_id: Dict[str, int],
    req: Dict[str, object],
):
    from_name = req["from_name"]  # type: ignore
    to_name = req["to_name"]      # type: ignore
    prios = req["priorities"]     # type: ignore

    if from_name not in name_to_id or to_name not in name_to_id:
        # unreachable / invalid
        return {
            "D": None,
            "V": None,
            "C": None,
            "COMP": None,
        }

    start = name_to_id[from_name]
    end = name_to_id[to_name]

    pathD_ids, sumsD = graph.dijkstra(start, end, "D")
    pathV_ids, sumsV = graph.dijkstra(start, end, "V")
    pathC_ids, sumsC = graph.dijkstra(start, end, "C")

    weights = priorities_to_weights(prios)
    pathComp_ids, sumsComp = graph.dijkstra(start, end, "COMBO", weights)

    def ids_to_names(ids: List[int]) -> List[str]:
        return [id_to_name[i] for i in ids]

    res = {
        "D": {
            "path": ids_to_names(pathD_ids) if pathD_ids else None,
            "sums": sumsD,
        },
        "V": {
            "path": ids_to_names(pathV_ids) if pathV_ids else None,
            "sums": sumsV,
        },
        "C": {
            "path": ids_to_names(pathC_ids) if pathC_ids else None,
            "sums": sumsC,
        },
        "COMP": {
            "path": ids_to_names(pathComp_ids) if pathComp_ids else None,
            "sums": sumsComp,
        },
    }
    return res


def format_route_line(criterion: str, route) -> str:
    """
    route: {"path": List[str] | None, "sums": {"D":..,"V":..,"C":..}}
    """
    if route is None or route["path"] is None:
        return f"{criterion}: ПУТЬ НЕ НАЙДЕН"

    path = route["path"]
    sums = route["sums"]
    return (
        f"{criterion}: " +
        " -> ".join(path) +
        f" | Д={sums['D']}, В={sums['V']}, С={sums['C']}"
    )


def main():
    input_file = "input.txt"
    output_file = "output.txt"

    graph, id_to_name, name_to_id, requests = parse_input(input_file)

    out_lines: List[str] = []
    for idx, req in enumerate(requests):
        routes = build_routes_for_request(graph, id_to_name, name_to_id, req)
        out_lines.append(format_route_line("ДЛИНА", routes["D"]))
        out_lines.append(format_route_line("ВРЕМЯ", routes["V"]))
        out_lines.append(format_route_line("СТОИМОСТЬ", routes["C"]))
        out_lines.append(format_route_line("КОМПРОМИСС", routes["COMP"]))
        if idx + 1 < len(requests):
            out_lines.append("")  # пустая строка между запросами

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))


if __name__ == "__main__":
    # ускоряем немного ввод/вывод
    sys.setrecursionlimit(1_000_000)
    main()