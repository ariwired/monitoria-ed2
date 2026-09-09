"""
Questão 4: Árvore Simétrica

Esta animação representa visualmente a lógica da resolução, mas não reproduz
cada chamada recursiva de forma literal.

O estado de no1/no2 e a pilha de chamadas pendentes são apresentados durante
a execução. Os nós permanecem destacados enquanto estão sendo comparados.

Os casos _espelho(None, None) são resumidos nas legendas, e o caso
não-simétrico retoma diretamente no ponto em que a comparação falha.

Como há valores repetidos na árvore, os nós usam identificadores internos
únicos apenas para a construção da animação.

Renderizar com:

    manim -pql animacoes/resolucao_lista1_professor/questao_04_arvoresimetrica.py Questao4ArvoreSimetrica
"""

from manim import *
from manim_dsa import *
from manim_dsa.utils.utils import set_text


class Questao4ArvoreSimetrica(Scene):
    def construct(self):
        titulo = Text(
            "Questão 4: Árvore Simétrica",
            font_size=32,
        ).to_edge(UP)

        self.play(Write(titulo), run_time=1.5)

        estrutura_arvore = {
            "raiz": ["esq", "dir"],
            "esq": ["esq_e", "esq_d"],
            "dir": ["dir_e", "dir_d"],
            "esq_e": [],
            "esq_d": [],
            "dir_e": [],
            "dir_d": [],
        }

        valores_reais = {
            "raiz": "1",
            "esq": "2",
            "dir": "2",
            "esq_e": "3",
            "esq_d": "4",
            "dir_e": "4",
            "dir_d": "3",
        }

        arvore_mob = (
            MTree(estrutura_arvore, root="raiz")
            .scale(0.62)
            .shift(DOWN * 0.15)
        )

        for chave, valor in valores_reais.items():
            no = arvore_mob.nodes[chave]
            no.label.become(set_text(no.label, valor))

        self.play(Create(arvore_mob), run_time=2.0)
        self.wait(1.5)

        texto_no1 = Text(
            "no1: raiz.esq",
            font_size=24,
        ).to_corner(DL).shift(UP * 0.7)

        ancora_no1 = texto_no1.get_left()

        texto_no2 = Text(
            "no2: raiz.dir",
            font_size=24,
        ).next_to(
            texto_no1,
            DOWN,
            buff=0.3,
            aligned_edge=LEFT,
        )

        ancora_no2 = texto_no2.get_left()

        def texto_ponteiro(nome, valor, ancora):
            return Text(
                f"{nome}: {valor}",
                font_size=24,
            ).move_to(
                ancora,
                aligned_edge=LEFT,
            )

        self.play(
            Write(texto_no1),
            Write(texto_no2),
            run_time=1.5,
        )

        pendentes = []

        def texto_pilha_atual():
            conteudo = ", ".join(pendentes)

            return Text(
                f"pilha: [{conteudo}]",
                font_size=18,
            ).to_corner(UR).shift(DOWN * 0.85)

        texto_pilha = texto_pilha_atual()
        self.play(Write(texto_pilha), run_time=1.0)

        def iniciar_comparacao(v1, v2, cor=YELLOW):
            return [
                arvore_mob.nodes[v].animate.highlight(cor)
                for v in (v1, v2)
                if v
            ]

        def encerrar_comparacao(v1, v2):
            return [
                arvore_mob.nodes[v].animate.unhighlight()
                for v in (v1, v2)
                if v
            ]

        self.play(
            *iniciar_comparacao("esq", "dir"),
            run_time=1.3,
        )

        self.play(
            Transform(
                texto_no1,
                texto_ponteiro("no1", "esq", ancora_no1),
            ),
            Transform(
                texto_no2,
                texto_ponteiro("no2", "dir", ancora_no2),
            ),
            run_time=1.3,
        )

        pendentes.append("(esq, dir)")

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            run_time=1.0,
        )

        self.wait(2.0)

        self.play(
            *encerrar_comparacao("esq", "dir"),
            run_time=1.0,
        )

        self.play(
            *iniciar_comparacao("esq_e", "dir_d"),
            run_time=1.3,
        )

        self.play(
            Transform(
                texto_no1,
                texto_ponteiro("no1", "esq_e", ancora_no1),
            ),
            Transform(
                texto_no2,
                texto_ponteiro("no2", "dir_d", ancora_no2),
            ),
            run_time=1.3,
        )

        pendentes.append("(esq_e, dir_d)")

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            run_time=1.0,
        )

        texto_ok1 = Text(
            "3 == 3; ambos None nos filhos",
            font_size=22,
        ).to_edge(DOWN)

        self.play(Write(texto_ok1), run_time=1.2)
        self.wait(2.4)

        pendentes.pop()

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            FadeOut(texto_ok1),
            *encerrar_comparacao("esq_e", "dir_d"),
            run_time=1.2,
        )

        self.play(
            *iniciar_comparacao("esq_d", "dir_e"),
            run_time=1.3,
        )

        self.play(
            Transform(
                texto_no1,
                texto_ponteiro("no1", "esq_d", ancora_no1),
            ),
            Transform(
                texto_no2,
                texto_ponteiro("no2", "dir_e", ancora_no2),
            ),
            run_time=1.3,
        )

        pendentes.append("(esq_d, dir_e)")

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            run_time=1.0,
        )

        texto_ok2 = Text(
            "4 == 4; ambos None nos filhos",
            font_size=22,
        ).to_edge(DOWN)

        self.play(Write(texto_ok2), run_time=1.2)
        self.wait(2.4)

        pendentes.pop()

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            FadeOut(texto_ok2),
            *encerrar_comparacao("esq_d", "dir_e"),
            run_time=1.2,
        )

        pendentes.pop()

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            run_time=1.0,
        )

        resultado = Text(
            "eh_simetrica() -> True",
            font_size=30,
            color=GREEN,
        ).to_edge(DOWN)

        self.play(Write(resultado), run_time=1.3)
        self.wait(2.5)
        self.play(FadeOut(resultado), run_time=1.0)

        aviso = Text(
            "Alterando dir_d: 3 -> 99",
            font_size=24,
            color=RED,
        ).to_edge(DOWN)

        self.play(Write(aviso), run_time=1.2)
        self.wait(1.2)

        no_dir_d = arvore_mob.nodes["dir_d"]

        label_99 = set_text(
            no_dir_d.label,
            "99",
        )

        self.play(
            Transform(
                no_dir_d.label,
                label_99,
                run_time=1.8,
            ),
            no_dir_d.circle.animate(
                run_time=1.8
            ).set_color(RED),
        )

        # Garante que o valor final permaneça visível.
        no_dir_d.label.become(
            set_text(no_dir_d.label, "99")
        )

        self.wait(1.8)
        self.play(FadeOut(aviso), run_time=1.0)

        self.play(
            Transform(
                texto_no1,
                texto_ponteiro("no1", "esq_e", ancora_no1),
            ),
            Transform(
                texto_no2,
                texto_ponteiro("no2", "dir_d", ancora_no2),
            ),
            run_time=1.3,
        )

        pendentes.append("(esq_e, dir_d)")

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            run_time=1.0,
        )

        self.play(
            *iniciar_comparacao(
                "esq_e",
                "dir_d",
                cor=RED,
            ),
            run_time=1.3,
        )

        self.wait(1.5)

        falha = Text(
            "3 != 99 -> espelho() retorna False",
            font_size=24,
            color=RED,
        ).to_edge(DOWN)

        self.play(Write(falha), run_time=1.3)
        self.wait(2.5)

        pendentes.pop()

        self.play(
            Transform(texto_pilha, texto_pilha_atual()),
            *encerrar_comparacao("esq_e", "dir_d"),
            run_time=1.2,
        )

        resultado_falso = Text(
            "eh_simetrica() -> False",
            font_size=30,
            color=RED,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(
                falha,
                resultado_falso,
            ),
            run_time=1.3,
        )

        self.wait(3.0)