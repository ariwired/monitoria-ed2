"""
Animação para a Questão 2 de Caminho de Soma Máxima.

Visualiza o backtracking:
  - MTree: destaca o nó sendo visitado e o(s) melhor(es) caminho(s) encontrado(s).
  - MStack: representa o caminho atual, com append() ao descer e pop() ao retroceder.
  - MVariable: mostra a soma atual e a melhor soma sendo atualizadas em tempo real.

Esta animação é apenas uma representação visual do algoritmo. A lógica aqui é reescrita de forma equivalente apenas para fins didáticos e de renderização.

Renderizar com:
    manim -pql animacoes/resolucao_lista1_professor/questao_02_caminhosomamaxima.py CaminhoSomaMaxima
"""

from manim import *
from manim_dsa import *

# Árvore usada no exemplo com os mesmos valores do notebook da Questão 2:

#
#          10
#         /  \
#        5    15
#       / \     \
#      3   7     20
#

# Os nomes dos nós no MTree precisam ser strings; usamos o próprio valor numérico como nome, já que são todos únicos nesta árvore de exemplo.

TREE = {
    "10": ["5", "15"],
    "5": ["3", "7"],
    "15": ["20"],
    "3": [],
    "7": [],
    "20": [],
}


class CaminhoSomaMaxima(Scene):
    """
        Anima o DFS com backtracking da Questão 2 sobre a árvore de exemplo.
    """

    def construct(self):
        titulo = Text("Questão 2: Caminho de Soma Máxima", font="Cascadia Code",).scale(0.5).to_edge(UP)
        self.play(Write(titulo))

        mTree = (
            MTree(TREE, root="10").scale(0.9).to_edge(LEFT, buff=1.3)
        )

        mStack = (
            MStack(style=MStackStyle.GREEN)
            .scale(0.75)
            .add_label(Text("caminho_atual", font="Cascadia Code").scale(0.5), UP)
            .to_edge(RIGHT, buff=1.8)
            .shift(UP * 1.2)
        )
        soma_var = (
            MVariable(0, style=MVariableStyle.BLUE)
            .scale(0.8)
            .add_label(Text("soma_atual", font="Cascadia Code").scale(0.45), LEFT)
            .next_to(mStack, DOWN, buff=1.0)
        )
        melhor_var = (
            MVariable("-inf", style=MVariableStyle.PURPLE)
            .scale(0.8)
            .add_label(Text("melhor_soma", font="Cascadia Code").scale(0.45), LEFT)
            .next_to(soma_var, DOWN, buff=0.8)
        )

        self.play(Create(mTree))
        self.play(Create(mStack), Create(soma_var), Create(melhor_var))
        self.wait()

        self.melhor_soma = float("-inf")
        self.melhor_caminho = []

        self._dfs(
            no="10",
            mTree=mTree,
            mStack=mStack,
            soma_var=soma_var,
            melhor_var=melhor_var,
            caminho_atual=[],
            soma_atual=0,
        )

        resultado = Text(f"melhor_caminho = {self.melhor_caminho}    soma = {int(self.melhor_soma)}", font="Cascadia Code",).scale(0.55).to_edge(DOWN)

        self.play(Write(resultado))
        self.wait(2)

    def _dfs(self, no, mTree, mStack, soma_var, melhor_var, caminho_atual, soma_atual):
        """
            Representa visualmente o DFS da Questão 2.

            A implementação é adaptada para fins de animação: o estado do melhor caminho é mantido na própria cena para permitir a atualização dos elementos visuais durante a travessia.
        """

        self.play(
            mTree[no].animate.highlight(),
            mStack.animate.append(no),
        )
        caminho_atual.append(int(no))
        soma_atual += int(no)
        self.play(soma_var.animate.set_value(soma_atual))

        filhos = TREE[no]

        if not filhos:
            if soma_atual > self.melhor_soma:
                caminho_anterior = self.melhor_caminho.copy()

                self.melhor_soma = soma_atual
                self.melhor_caminho = caminho_atual.copy()
                self.play(melhor_var.animate.set_value(int(soma_atual)))

                nos_a_desmarcar = [v for v in caminho_anterior if v not in self.melhor_caminho]

                if nos_a_desmarcar:
                    self.play(
                        *[mTree[str(v)].animate.unhighlight() for v in nos_a_desmarcar]
                    )

                self.play(
                    *[mTree[str(v)].animate.highlight(GOLD) for v in caminho_atual]
                )
        else:
            for filho in filhos:
                self._dfs(
                    filho, mTree, mStack, soma_var, melhor_var,
                    caminho_atual, soma_atual,
                )

        caminho_atual.pop()
        soma_apos_pop = soma_atual - int(no)

        self.play(
            mStack.animate.pop(),
            soma_var.animate.set_value(soma_apos_pop),
        )
        if int(no) not in self.melhor_caminho:
            self.play(mTree[no].animate.unhighlight())