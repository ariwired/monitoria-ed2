"""
Diferenças estruturais entre esta animação e a resolução real:

A resolução usa recursão sobre no.esquerda e no.direita. Na animação, uma MStack é utilizada apenas para tornar visível a pilha de chamadas recursivas, que na implementação real é gerenciada implicitamente pelo Python.

Ao finalizar um nó em pós-ordem, a resolução define no.esquerda e no.direita como None. Na animação, o esmaecimento do nó representa apenas que seu processamento foi concluído, e não uma remoção literal da memória.

NOTA TÉCNICA:
A árvore é representada visualmente com MGraph, usando uma lista de adjacência e posições manuais. Essa escolha permite controlar diretamente a disposição dos nós e manter a geometria típica de uma árvore binária.

Renderizar com:
    manim -pql animacoes/resolucao_lista_01_professor/questao_03_esvaziararvore.py Questao3EsvaziarArvore
"""

from manim import *
from manim_dsa import *


class Questao3EsvaziarArvore(Scene):
    """
        Cena que visualiza o esvaziamento de uma árvore binária em pós-ordem.

        Ordem de finalização esperada:
        10, 20, 40, 30, 60, 90, 80, 70, 50
    """

    def construct(self):
        titulo = Text(
            "Esvaziar Árvore: Percurso Pós-Ordem",
            font_size=32,
        ).to_edge(UP)
        self.play(Write(titulo))

        grafo = {
            "50": ["30", "70"],
            "30": ["50", "20", "40"],
            "70": ["50", "60", "80"],
            "20": ["30", "10"],
            "40": ["30"],
            "60": ["70"],
            "80": ["70", "90"],
            "10": ["20"],
            "90": ["80"],
        }

        posicoes = {
            "50": UP * 2.2,
            "30": UP * 1.0 + LEFT * 2.2,
            "70": UP * 1.0 + RIGHT * 2.2,
            "20": DOWN * 0.2 + LEFT * 3.3,
            "40": DOWN * 0.2 + LEFT * 1.1,
            "60": DOWN * 0.2 + RIGHT * 1.1,
            "80": DOWN * 0.2 + RIGHT * 3.3,
            "10": DOWN * 1.4 + LEFT * 3.3,
            "90": DOWN * 1.4 + RIGHT * 3.3,
        }

        arvore_mobj = (
            MGraph(grafo, posicoes, style=MGraphStyle.PURPLE)
            .scale(0.75)
            .shift(LEFT * 3.2 + DOWN * 0.3)
        )

        self.play(Create(arvore_mobj))
        self.wait(0.5)

        pilha_recursao = MStack().shift(RIGHT * 4.5)

        rotulo_pilha = Text("Pilha de recursão", font_size=24).next_to(
            pilha_recursao, UP
        )

        self.play(Create(pilha_recursao), Write(rotulo_pilha))

        rotulo_status = Text(
            "Descendo: pos_ordem_limpar(50)", font_size=22
        ).to_edge(DOWN)
        self.play(Write(rotulo_status))

        ordem_visita = [
            ("empilha", 50, "chamando pos_ordem_limpar(50)"),
            ("empilha", 30, "descendo pela esquerda: pos_ordem_limpar(30)"),
            ("empilha", 20, "descendo pela esquerda: pos_ordem_limpar(20)"),
            ("empilha", 10, "descendo pela esquerda: pos_ordem_limpar(10)"),
            ("finaliza", 10, "10 sem filhos -> finaliza 10 (L de 20 concluído)"),
            ("desempilha", 10, "retorna de pos_ordem_limpar(10)"),
            ("finaliza", 20, "L e R de 20 concluídos -> finaliza 20"),
            ("desempilha", 20, "retorna de pos_ordem_limpar(20) — L de 30 concluído"),
            ("empilha", 40, "descendo pela direita: pos_ordem_limpar(40)"),
            ("finaliza", 40, "40 sem filhos -> finaliza 40 (R de 30 concluído)"),
            ("desempilha", 40, "retorna de pos_ordem_limpar(40)"),
            ("finaliza", 30, "L e R de 30 já processados -> finaliza 30"),
            ("desempilha", 30, "retorna de pos_ordem_limpar(30) — L de 50 concluído"),
            ("empilha", 70, "descendo pela direita: pos_ordem_limpar(70)"),
            ("empilha", 60, "descendo pela esquerda: pos_ordem_limpar(60)"),
            ("finaliza", 60, "60 sem filhos -> finaliza 60 (L de 70 concluído)"),
            ("desempilha", 60, "retorna de pos_ordem_limpar(60)"),
            ("empilha", 80, "descendo pela direita: pos_ordem_limpar(80)"),
            ("empilha", 90, "descendo pela direita: pos_ordem_limpar(90)"),
            ("finaliza", 90, "90 sem filhos -> finaliza 90 (R de 80 concluído)"),
            ("desempilha", 90, "retorna de pos_ordem_limpar(90)"),
            ("finaliza", 80, "L e R de 80 já processados -> finaliza 80"),
            ("desempilha", 80, "retorna de pos_ordem_limpar(80) — R de 70 concluído"),
            ("finaliza", 70, "L e R de 70 já processados -> finaliza 70 (R de 50 concluído)"),
            ("desempilha", 70, "retorna de pos_ordem_limpar(70)"),
            ("finaliza", 50, "L e R de 50 já processados -> finaliza 50 (raiz)"),
            ("desempilha", 50, "retorna de pos_ordem_limpar(50) — árvore vazia"),
        ]

        for acao, valor, texto in ordem_visita:
            novo_status = Text(texto, font_size=22).to_edge(DOWN)

            if acao == "empilha":
                self.play(
                    pilha_recursao.animate.append(str(valor)),
                    Transform(rotulo_status, novo_status),
                    run_time=1.4,
                )
                self.wait(1.5)

            elif acao == "desempilha":
                self.play(
                    pilha_recursao.animate.pop(),
                    Transform(rotulo_status, novo_status),
                    run_time=1.3,
                )
                self.wait(1.0)

            elif acao == "finaliza":
                self.play(
                    arvore_mobj[str(valor)].animate.set_opacity(0.15),
                    Transform(rotulo_status, novo_status),
                    run_time=1.8,
                )
                self.wait(2.5)

        texto_final = Text(
            "self.raiz = None: árvore vazia",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN)

        self.play(Transform(rotulo_status, texto_final))
        self.wait(3.0)