import discord
import asyncio
from typing import Callable, Awaitable

class DiscordCloner:
    def __init__(self):
        self.client: discord.Client | None = None
        self.user = None

    async def login(self, token: str):
        """User Tokenでログイン"""
        self.client = discord.Client()
        try:
            await self.client.start(token)
        except Exception as e:
            raise RuntimeError(f"ログイン失敗: {e}")

    async def get_guilds(self, token: str):
        """参加サーバー一覧を取得（別クライアントで取得）"""
        client = discord.Client()
        guilds_data = []

        @client.event
        async def on_ready():
            for g in client.guilds:
                guilds_data.append({
                    "id": str(g.id),
                    "name": g.name,
                    "icon": str(g.icon.url) if g.icon else None,
                    "member_count": g.member_count,
                })
            await client.close()

        await client.start(token)
        return guilds_data

    async def clone(
        self,
        token: str,
        src_id: int,
        dst_id: int,
        options: dict,
        progress_cb: Callable[[str, int], Awaitable[None]],
    ):
        """サーバーを複製する"""
        client = discord.Client()

        @client.event
        async def on_ready():
            try:
                src = client.get_guild(src_id)
                dst = client.get_guild(dst_id)

                if not src or not dst:
                    await progress_cb("❌ サーバーが見つかりません", 0)
                    await client.close()
                    return

                if src.id == dst.id:
                    await progress_cb("❌ 複製元と複製先が同じです", 0)
                    await client.close()
                    return

                total_steps = sum([
                    1 if options.get("roles") else 0,
                    1 if options.get("categories") else 0,
                    1 if options.get("text_channels") else 0,
                    1 if options.get("voice_channels") else 0,
                    1 if options.get("messages") else 0,
                ])
                step = 0

                # ── ロール複製 ──
                if options.get("roles"):
                    await progress_cb("🎭 ロールを複製中...", int(step / total_steps * 100))
                    for role in reversed(src.roles):
                        if role.is_default() or role.managed:
                            continue
                        try:
                            await dst.create_role(
                                name=role.name,
                                permissions=role.permissions,
                                colour=role.colour,
                                hoist=role.hoist,
                                mentionable=role.mentionable,
                            )
                        except Exception as e:
                            await progress_cb(f"⚠️ ロール作成失敗 {role.name}: {e}", int(step / total_steps * 100))
                        await asyncio.sleep(0.3)
                    step += 1

                # ── カテゴリ複製 ──
                category_map = {}
                if options.get("categories"):
                    await progress_cb("📁 カテゴリを複製中...", int(step / total_steps * 100))
                    for cat in src.categories:
                        try:
                            new_cat = await dst.create_category(
                                name=cat.name,
                                overwrites=cat.overwrites,
                                position=cat.position,
                            )
                            category_map[cat.id] = new_cat
                        except Exception as e:
                            await progress_cb(f"⚠️ カテゴリ作成失敗 {cat.name}: {e}", int(step / total_steps * 100))
                        await asyncio.sleep(0.3)
                    step += 1

                # ── テキストチャンネル ──
                if options.get("text_channels"):
                    await progress_cb("💬 テキストチャンネルを複製中...", int(step / total_steps * 100))
                    for ch in src.text_channels:
                        try:
                            parent = category_map.get(ch.category_id) if ch.category_id else None
                            await dst.create_text_channel(
                                name=ch.name,
                                topic=ch.topic,
                                slowmode_delay=ch.slowmode_delay,
                                nsfw=ch.nsfw,
                                position=ch.position,
                                category=parent,
                            )
                        except Exception as e:
                            await progress_cb(f"⚠️ チャンネル作成失敗 {ch.name}: {e}", int(step / total_steps * 100))
                        await asyncio.sleep(0.3)
                    step += 1

                # ── ボイスチャンネル ──
                if options.get("voice_channels"):
                    await progress_cb("🔊 ボイスチャンネルを複製中...", int(step / total_steps * 100))
                    for ch in src.voice_channels:
                        try:
                            parent = category_map.get(ch.category_id) if ch.category_id else None
                            await dst.create_voice_channel(
                                name=ch.name,
                                bitrate=ch.bitrate,
                                user_limit=ch.user_limit,
                                position=ch.position,
                                category=parent,
                            )
                        except Exception as e:
                            await progress_cb(f"⚠️ VC作成失敗 {ch.name}: {e}", int(step / total_steps * 100))
                        await asyncio.sleep(0.3)
                    step += 1

                # ── メッセージ ──
                if options.get("messages"):
                    limit = int(options.get("message_limit", 100))
                    await progress_cb(f"📨 メッセージを複製中（最大{limit}件/チャンネル）...", int(step / total_steps * 100))

                    dst_text_map = {c.name: c for c in dst.text_channels}

                    for src_ch in src.text_channels:
                        dst_ch = dst_text_map.get(src_ch.name)
                        if not dst_ch:
                            continue
                        try:
                            msgs = []
                            async for m in src_ch.history(limit=limit, oldest_first=True):
                                msgs.append(m)
                            for m in msgs:
                                content = f"**{m.author.display_name}**: {m.content}"
                                if m.attachments:
                                    content += "\n" + "\n".join(a.url for a in m.attachments)
                                if not content.strip():
                                    continue
                                try:
                                    await dst_ch.send(content)
                                    await asyncio.sleep(1.2)  # レート制限対策
                                except Exception:
                                    await asyncio.sleep(3)
                        except Exception as e:
                            await progress_cb(f"⚠️ メッセージ取得失敗 {src_ch.name}: {e}", int(step / total_steps * 100))
                    step += 1

                await progress_cb("✅ 完了しました！", 100)
                await client.close()

            except Exception as e:
                await progress_cb(f"❌ エラー: {e}", 0)
                try:
                    await client.close()
                except Exception:
                    pass

        await client.start(token)
