create extension if not exists pgcrypto;

create table public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null check (char_length(display_name) between 1 and 40),
  avatar_id text,
  locale text not null default 'en-US',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.game_saves (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  slot smallint not null check (slot between 1 and 5),
  save_version integer not null check (save_version > 0),
  revision bigint not null default 1 check (revision > 0),
  company_name text not null check (char_length(company_name) between 1 and 40),
  facility_tier smallint not null default 1 check (facility_tier between 1 and 6),
  state jsonb not null check (jsonb_typeof(state) = 'object' and pg_column_size(state) <= 1048576),
  checksum text not null check (checksum ~ '^[a-f0-9]{64}$'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, slot)
);

create table public.player_settings (
  user_id uuid primary key references auth.users(id) on delete cascade,
  control_mode text not null default 'keyboard' check (control_mode in ('keyboard','gamepad','phone')),
  music_volume numeric(4,3) not null default 0.75 check (music_volume between 0 and 1),
  voice_volume numeric(4,3) not null default 0.9 check (voice_volume between 0 and 1),
  sfx_volume numeric(4,3) not null default 0.85 check (sfx_volume between 0 and 1),
  captions boolean not null default true,
  reduced_motion boolean not null default false,
  updated_at timestamptz not null default now()
);

create table public.support_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  category text not null check (category in ('bug','account','save','accessibility','feedback')),
  message text not null check (char_length(message) between 1 and 4000),
  status text not null default 'open' check (status in ('open','triaged','resolved')),
  created_at timestamptz not null default now()
);

create or replace function public.set_updated_at() returns trigger language plpgsql
security invoker set search_path = '' as $$
begin new.updated_at = now(); return new; end;
$$;

create trigger profiles_updated_at before update on public.profiles for each row execute function public.set_updated_at();
create trigger game_saves_updated_at before update on public.game_saves for each row execute function public.set_updated_at();
create trigger player_settings_updated_at before update on public.player_settings for each row execute function public.set_updated_at();

alter table public.profiles enable row level security;
alter table public.game_saves enable row level security;
alter table public.player_settings enable row level security;
alter table public.support_requests enable row level security;

create policy "profiles_owner_select" on public.profiles for select to authenticated using ((select auth.uid()) = user_id);
create policy "profiles_owner_insert" on public.profiles for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "profiles_owner_update" on public.profiles for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "profiles_owner_delete" on public.profiles for delete to authenticated using ((select auth.uid()) = user_id);

create policy "saves_owner_select" on public.game_saves for select to authenticated using ((select auth.uid()) = user_id);
create policy "saves_owner_insert" on public.game_saves for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "saves_owner_update" on public.game_saves for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "saves_owner_delete" on public.game_saves for delete to authenticated using ((select auth.uid()) = user_id);

create policy "settings_owner_select" on public.player_settings for select to authenticated using ((select auth.uid()) = user_id);
create policy "settings_owner_insert" on public.player_settings for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "settings_owner_update" on public.player_settings for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "settings_owner_delete" on public.player_settings for delete to authenticated using ((select auth.uid()) = user_id);

create policy "support_owner_insert" on public.support_requests for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "support_owner_select" on public.support_requests for select to authenticated using ((select auth.uid()) = user_id);

revoke all on public.profiles, public.game_saves, public.player_settings, public.support_requests from anon;
grant select, insert, update, delete on public.profiles, public.game_saves, public.player_settings to authenticated;
grant select, insert on public.support_requests to authenticated;
